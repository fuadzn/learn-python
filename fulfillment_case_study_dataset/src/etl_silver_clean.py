import json
import pandas as pd
from pathlib import Path

# Define Path relative to project root (one level up from src/)
PROJECT_ROOT = Path(__file__).parent.parent
BRONZE_DIR = PROJECT_ROOT / 'data' / 'bronze'
SILVER_DIR = PROJECT_ROOT / 'data' / 'silver'
GOLD_DIR = PROJECT_ROOT / 'data' / 'gold'

SILVER_DIR.mkdir(parents=True,exist_ok=True)
GOLD_DIR.mkdir(parents=True,exist_ok=True)

# Read raw JSONL events
raw_records = []
with open(BRONZE_DIR / "wms_scanner_events_raw.jsonl", "r") as f:
    for line in f:
        raw_records.append(json.loads(line))

# Flatten nested payload struct
flattened = []
gold = []

for row in raw_records:
    flat_row = {
        "event_id": row.get("event_id"),
        "order_id": row.get("order_id"),
        "ingested_at": row.get("ingested_at"),
        "warehouse_id": row["payload"].get("warehouse_id"),
        "stage_name": row["payload"].get("stage_name"),
        "stage_timestamp": row["payload"].get("event_ts"),
        "timezone": row["payload"].get("timezone"),
        "scanner_device_id": row["payload"].get("scanner_device_id"),
        "is_multi_item_queue": row["payload"].get("is_multi_item_queue"),
    }
    # Data Quality Rule: Gold records with missing primary/foreign keys
    if flat_row["order_id"] is None or flat_row["event_id"] is None:
        gold.append(flat_row)
    else:
        flattened.append(flat_row)

df_gold = pd.DataFrame(gold)
df_gold.to_csv(GOLD_DIR / "wms_gold_events.csv", index=False)

# Duplicate webhook retries (keep latest ingested_at per event_id)
df_valid = pd.DataFrame(flattened)
df_silver = (
    df_valid.sort_values("ingested_at", ascending=False)
    .drop_duplicates(subset=["event_id"], keep="first")
    .sort_values(["order_id", "stage_timestamp"])
)

# Save clean Silver layer as Parquet (and CSV for easy inspection)
df_silver.to_parquet(SILVER_DIR / "wms_silver_events.parquet", index=False)
df_silver.to_csv(SILVER_DIR / "wms_silver_events.csv", index=False)

print(f"Raw events processed: {len(raw_records)}")
print(f"Gold (bad records): {len(df_gold)}")
print(f"Duplicate removed: {len(df_valid) - len(df_silver)}")
print(f"Silver (clean): {len(df_silver)}")