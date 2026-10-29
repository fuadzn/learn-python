import duckdb
from pathlib import Path

# Resolve paths relative to project root (one level up from src/)
PROJECT_ROOT = Path(__file__).parent.parent
BRONZE = str(PROJECT_ROOT / 'data' / 'bronze')
SILVER = str(PROJECT_ROOT / 'data' / 'silver')

# Connect to db
con = duckdb.connect(str(PROJECT_ROOT / "warehouse.duckdb"))

# Load dimension & Fact tables into the Gold schema
con.execute(f"""
    CREATE OR REPLACE TABLE dim_warehouse AS
    SELECT * FROM read_csv_auto('{BRONZE}/dim_warehouses.csv');

    CREATE OR REPLACE TABLE dim_couriers AS
    SELECT * FROM read_csv_auto('{BRONZE}/dim_couriers.csv');
    
    CREATE OR REPLACE TABLE fact_orders AS
    SELECT * FROM read_csv_auto('{BRONZE}/oms_orders_raw.csv');

    CREATE OR REPLACE TABLE fact_order_events AS
    SELECT * FROM read_parquet('{SILVER}/wms_silver_events.parquet');
""")

# Run SQL Window Function Analysis to find the operational bottleneck
bottleneck_sql = """
WITH stage_transitions AS (
    SELECT 
        e.order_id,
        e.warehouse_id,
        w.city,
        e.stage_name,
        CAST(e.stage_timestamp as TIMESTAMP) as stage_ts,
        LEAD(CAST(e.stage_timestamp as TIMESTAMP)) OVER (
            PARTITION BY e.order_id ORDER BY CAST(e.stage_timestamp AS TIMESTAMP)
        ) AS next_stage_ts,
        e.is_multi_item_queue
    FROM fact_order_events e
    JOIN dim_warehouse w ON e.warehouse_id = w.warehouse_id
)
SELECT 
    warehouse_id,
    city,
    stage_name as current_stage,
    COUNT(order_id) AS total_orders,
    ROUND(AVG(date_diff('second', stage_ts, next_stage_ts) / 60.0), 2) AS avg_dwell_mins,
    ROUND(QUANTILE_CONT( date_diff('second', stage_ts, next_stage_ts) / 60.0, 0.95), 2) AS p95_dwell_mins
FROM stage_transitions
WHERE next_stage_ts IS NOT NULL
    AND stage_name IN ('ORDER_PLACED', 'PICKED', 'PACKED')
GROUP BY warehouse_id, city, stage_name
ORDER BY p95_dwell_mins DESC;
"""

df_results = con.execute(bottleneck_sql).df()
print("\n=== GOLD LAYER:  STAGE DWELL TIME BOTTLENECK ANALYSIS ===")
print(df_results.to_string(index=False))

# Drill-Down SQL: Prove the Root Cause (Afternoon Peak + Multi-Item Queue)
root_cause_sql = """
WITH picked_to_packed AS (
    SELECT
        e.warehouse_id,
        o.service_tier,
        o.is_multi_item,
        o.primary_category,
        EXTRACT(HOUR FROM CAST(e.stage_timestamp AS TIMESTAMP)) AS pick_hour,
        CAST(e.stage_timestamp AS TIMESTAMP) AS pick_ts,
        LEAD(CAST(e.stage_timestamp AS TIMESTAMP)) OVER (PARTITION BY e.order_id ORDER BY CAST(e.stage_timestamp AS TIMESTAMP)) AS packed_ts
    FROM fact_order_events e
    JOIN fact_orders o ON e.order_id = o.order_id
    WHERE e.stage_name IN ('PICKED', 'PACKED')
)
SELECT 
    warehouse_id,
    CASE WHEN pick_hour BETWEEN 14 AND 17 then 'PEAK (14:00-17:00)' ELSE 'Off-Peak' END AS time_window,
    is_multi_item,
    COUNT(*) AS orders,
    ROUND(AVG(date_diff('second', pick_ts, packed_ts) / 60.0), 2) AS avg_pack_wait_mins,
    ROUND(QUANTILE_CONT(date_diff('second', pick_ts, packed_ts) / 60.0, 0.95), 2) AS p95_pack_wait_mins
FROM picked_to_packed
WHERE packed_ts IS NOT NULL
    AND warehouse_id IN ('WH-JKT-01','WH-BDG-02')
GROUP BY 1,2,3
ORDER BY p95_pack_wait_mins DESC;
"""

df_root_cause = con.execute(root_cause_sql).df()
print("\n=== ROOT CAUSE DRILL-DOWN: PEAK HOURS VS MULTI-ITEM QUEUE ===")
print(df_root_cause.to_string(index=False))