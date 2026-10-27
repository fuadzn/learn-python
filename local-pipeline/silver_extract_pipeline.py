import subprocess
import re
import polars as pl
from pydantic import BaseModel
from typing import Literal

# 1. Kontrak Data (Skema Tabel Silver)
class LogExtraction(BaseModel):
    kategori: Literal["bug_report", "feature_request", "praise"]
    sentimen: Literal["positif", "netral", "negatif"]
    komponen: str
    skor_urgensi: int

def panggil_fm(prompt: str) -> str:
    """Mendeteksi dan menjalankan sub-command /usr/bin/fm secara otomatis."""
    kandidat_subcommand = [
        ["/usr/bin/fm", "prompt", prompt],
        ["/usr/bin/fm", "run", prompt],
        ["/usr/bin/fm", "generate", prompt],
        ["/usr/bin/fm", "respond", prompt],
        ["/usr/bin/fm", "chat", prompt],
        ["/usr/bin/fm", "-p", prompt],
    ]

    for cmd in kandidat_subcommand:
        res = subprocess.run(cmd, capture_output=True, text=True)
        # Jika sub-command dikenali dan menghasilkan teks
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()

    # Jika tidak ada yang cocok, tampilkan isi fm --help agar kita langsung tahu perintahnya
    help_res = subprocess.run(["/usr/bin/fm", "--help"], capture_output=True, text=True)
    help_text = (help_res.stdout or "") + (help_res.stderr or "")
    raise RuntimeError(
        "Sub-command untuk /usr/bin/fm berbeda. Ini daftar perintah dari 'fm --help':\n\n"
        f"{help_text}"
    )

# 2. Baca data mentah dari Bronze Layer
df_bronze = pl.read_parquet("bronze_logs.parquet")
extracted_rows = []

print("Memproses transformasi data menggunakan '/usr/bin/fm'...")

for row in df_bronze.iter_rows(named=True):
    prompt = (
        "Ubahlah log berikut menjadi format JSON murni satu baris tanpa penjelasan apa pun. "
        "Gunakan persis key berikut: "
        '{"kategori": "bug_report", "sentimen": "negatif", "komponen": "Database", "skor_urgensi": 5}. '
        "Aturan nilai: "
        "kategori hanya boleh 'bug_report', 'feature_request', atau 'praise'. "
        "sentimen hanya boleh 'positif', 'netral', atau 'negatif'. "
        "skor_urgensi harus angka bulat 1 sampai 5. "
        f'Log: "{row["raw_text"]}"'
    )

    raw_output = panggil_fm(prompt)

    # Ambil hanya blok JSON { ... } dari jawaban LLM
    match = re.search(r"\{.*?\}", raw_output, re.DOTALL)
    if not match:
        raise ValueError(f"Output dari fm bukan JSON valid untuk ID {row['id']}:\n{raw_output}")

    parsed = LogExtraction.model_validate_json(match.group(0))

    extracted_rows.append({
        "id": row["id"],
        "timestamp": row["timestamp"],
        "raw_text": row["raw_text"],
        **parsed.model_dump()
    })
    print(f"Log ID {row['id']} berhasil diekstrak -> {parsed.kategori} (Urgensi: {parsed.skor_urgensi})")

# 3. Simpan ke Silver Layer (Parquet)
df_silver = pl.DataFrame(extracted_rows)
df_silver.write_parquet("silver_logs_enriched.parquet")

print("\nSilver Layer selesai! Preview hasil transformasi:")
print(df_silver)