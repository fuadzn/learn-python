from pyspark.sql import SparkSession, Window
from pyspark.sql import functions as F
from pyspark.sql.types import (
    BooleanType,
    StringType,
    StructField,
    StructType,
)

# Define data path
BRONZE_DIR = "data/bronze"
SILVER_DIR = "data/silver"
GOLD_DIR = "data/gold"

spark = (
    SparkSession.builder.appName("wms_silver_job")
    .master("local[*]")
    .config("spark.sql.session.timeZone", "Asia/Jakarta")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

# Explicit schema for the raw JSONL (no inferSchema in production)
payload_schema = StructType([
    StructField("warehouse_id", StringType()),
    StructField("stage_name", StringType()),
    StructField("event_ts", StringType()),
    StructField("timezone", StringType()),
    StructField("scanner_device_id", StringType()),
    StructField("is_multi_item_queue", BooleanType()),
])

raw_schema = StructType([
    StructField("event_id", StringType()),
    StructField("order_id", StringType()),
    StructField("ingested_at", StringType()),
    StructField("payload", payload_schema),
])

# Read raw JSONL events
df_raw = spark.read.schema(raw_schema).json(f"{BRONZE_DIR}/wms_scanner_events_raw.jsonl")

# Flatten nested payload struct
df_flat = df_raw.select(
    "event_id",
    "order_id",
    F.to_timestamp("ingested_at").alias("ingested_at"),
    F.col("payload.warehouse_id").alias("warehouse_id"),
    F.col("payload.stage_name").alias("stage_name"),
    F.to_timestamp("payload.event_ts").alias("stage_timestamp"),
    F.col("payload.timezone").alias("timezone"),
    F.col("payload.scanner_device_id").alias("scanner_device_id"),
    F.col("payload.is_multi_item_queue").alias("is_multi_item_queue"),
).cache()

# Data Quality Rule: quarantine records with missing primary/foreign keys
is_bad = F.col("order_id").isNull() | F.col("event_id").isNull()
df_bad = df_flat.filter(is_bad)
df_valid = df_flat.filter(~is_bad)

df_bad.coalesce(1).write.mode("overwrite").option("header", True).csv(
    f"{GOLD_DIR}/wms_gold_events.csv"
)

# Duplicate webhook retries (keep latest ingested_at per event_id)
latest_first = Window.partitionBy("event_id").orderBy(F.col("ingested_at").desc())
df_silver = (
    df_valid.withColumn("rn", F.row_number().over(latest_first))
    .filter(F.col("rn") == 1)
    .drop("rn")
    .orderBy("order_id", "stage_timestamp")
)

# Save clean Silver layer as Parquet (and CSV for easy inspection)
df_silver.write.mode("overwrite").parquet(f"{SILVER_DIR}/wms_silver_events.parquet")
df_silver.coalesce(1).write.mode("overwrite").option("header", True).csv(
    f"{SILVER_DIR}/wms_silver_events.csv"
)

raw_count = df_flat.count()
bad_count = df_bad.count()
valid_count = df_valid.count()
silver_count = df_silver.count()

print(f"Raw events processed: {raw_count}")
print(f"Gold (bad records): {bad_count}")
print(f"Duplicate removed: {valid_count - silver_count}")
print(f"Silver (clean): {silver_count}")

spark.stop()
