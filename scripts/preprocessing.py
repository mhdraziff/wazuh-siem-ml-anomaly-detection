import pandas as pd
from konfigurasi import FILE_RAW, FILE_CLEAN
def preprocessing():
df_raw = pd.read_csv(FILE_RAW)
print(f"[INFO] Membaca dataset mentah: {FILE_RAW}")
print("[INFO] Total baris:", df_raw.shape[0])
# Buang baris yang kosong pada kolom penting
df = df_raw.dropna(subset=["timestamp",
"rule_description", "full_log"]).copy()
# Konversi timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"],
errors="coerce", utc=True)
df = df.dropna(subset=["timestamp"])
# Fitur jam
df["hour"] = df["timestamp"].dt.hour
# Fitur malam (00-05)
df["is_night"] = df["hour"].apply(lambda x: 1 if 0 <=
int(x) <= 5 else 0)
# Panjang log
df["log_length"] = df["full_log"].astype(str).apply(len)
# Apakah mengandung ssh/sshd
df["is_ssh"] = df.apply(
lambda row: 1 if ("ssh" in
str(row["rule_description"]).lower()
or "sshd" in
str(row["full_log"]).lower()) else 0,
axis=1
)
# Pastikan numerik
df["firedtimes"] = pd.to_numeric(df["firedtimes"],
errors="coerce").fillna(1).astype(int)
df["rule_level"] = pd.to_numeric(df["rule_level"],
errors="coerce").fillna(0).astype(int)
# Labeling: firedtimes > 10 atau rule_level >= 7 =
anomali
df["label"] = df.apply(
lambda row: 1 if (row["firedtimes"] > 10 or
row["rule_level"] >= 7) else 0,
axis=1
)
# Dataset final untuk ML
final_cols = ["firedtimes", "rule_level", "hour",
"is_night", "is_ssh", "log_length", "label"]
df_clean = df[final_cols].copy()
df_clean.to_csv(FILE_CLEAN, index=False)
print(f"✅ Dataset bersih disimpan: {FILE_CLEAN}")
print("[INFO] Distribusi label:")
print(df_clean["label"].value_counts())
print("[INFO] Contoh dataset clean (5 baris):")
print(df_clean.head())
print("[INFO] Total baris clean:", df_clean.shape[0])
if __name__ == "__main__":
preprocessing()
