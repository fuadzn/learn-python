import polars as pl
from datetime import datetime

raw_logs = [
    {"id": 101, "timestamp" : "2026-10-27T08:15:00", "raw_text": "Server DB timeout pas query tabel transaksi di region jakarta, user komplain gagal bayar!"},
    {"id": 102, "timestamp" : "2026-10-27T08:17:30", "raw_text": "Fitur dark mode baru keren banget, tampilannya jadi enak dilihat pas malam."},
    {"id": 103, "timestamp" : "2026-10-27T08:17:30", "raw_text": "Tolong tambahkan export laporan ke format Excel dong buat tim finance."},
    {"id": 104, "timestamp" : "2026-10-27T08:20:12", "raw_text": "API payment gateway error 502 terus dari pagi di aplikasi iOS, parah nih."},
]

df_bronze = pl.DataFrame(raw_logs).with_columns(
    pl.lit(datetime.now()).alias("ingestion_time")
)

# Save to file parquest
df_bronze.write_parquet("bronze_logs.parquet")
print("Bronze layer tersimpan: bronze_logs.parquet")