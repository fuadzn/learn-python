import duckdb

# Koneksi ke file database DuckDB lokal
con = duckdb.connect("warehouse.duckdb")

# 1. Buat tabel Silver dari file Parquet (Sesuaikan nama filenya)
con.execute("""
    CREATE OR REPLACE TABLE silver_logs AS 
    SELECT * FROM read_parquet('silver_logs_enriched.parquet')
""")

# 2. Buat tabel agregasi Gold menggunakan SQL
con.execute("""
    CREATE OR REPLACE TABLE gold_summary_by_category AS
    SELECT 
        kategori,
        sentimen,
        COUNT(*) AS total_laporan,
        ROUND(AVG(skor_urgensi), 2) AS rata_rata_urgensi,
        LIST(komponen) AS daftar_komponen
    FROM silver_logs
    GROUP BY kategori, sentimen
    ORDER BY rata_rata_urgensi DESC
""")

print("=== ISI TABEL SILVER (Hasil Ekstrak LLM) ===")
con.sql("SELECT id, kategori, sentimen, komponen, skor_urgensi FROM silver_logs").show()

print("=== ISI TABEL GOLD (Hasil Agregasi Analitik SQL) ===")
con.sql("SELECT * FROM gold_summary_by_category").show()