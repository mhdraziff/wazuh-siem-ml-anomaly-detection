import requests
import pandas as pd
from konfigurasi import ELASTIC_BASE_URL, INDEX_PATTERN,
FILE_RAW, JUMLAH_DATA
def ambil_data_elasticsearch():
url = f"{ELASTIC_BASE_URL}/{INDEX_PATTERN}/_search"
query = {
"size": JUMLAH_DATA,
"sort": [{"@timestamp": {"order": "desc"}}],
"query": {"match_all": {}}
}
print(f"[INFO] Mengambil data dari: {url}")
resp = requests.get(url, json=query, timeout=30)
if resp.status_code != 200:
print("[ERROR] Gagal ambil data!")
print(resp.status_code, resp.text[:300])
return None
data = resp.json()
hits = data.get("hits", {}).get("hits", [])
print(f"[INFO] Total dokumen diterima: {len(hits)}")
records = []
for hit in hits:
src = hit.get("_source", {})
record = {
"rule_level": src.get("rule", {}).get("level",
0),
"rule_id": src.get("rule", {}).get("id", ""),
"rule_description": src.get("rule",
{}).get("description", ""),
"firedtimes": src.get("rule",
{}).get("firedtimes", 1),
"timestamp": src.get("@timestamp", ""),
"agent_id": src.get("agent", {}).get("id", ""),
"agent_name": src.get("agent", {}).get("name",
""),
"agent_ip": src.get("agent", {}).get("ip", ""),
"full_log": src.get("full_log", ""),
"location": src.get("location", "")
}
records.append(record)
df_raw = pd.DataFrame(records)
return df_raw
if __name__ == "__main__":
df = ambil_data_elasticsearch()
if df is None or df.empty:
print("[INFO] Data kosong, tidak ada yang
disimpan.")
raise SystemExit(0)
df.to_csv(FILE_RAW, index=False)
print(f"✅ Data mentah disimpan: {FILE_RAW}")
print("[INFO] Contoh 5 baris pertama:")
print(df.head())
print("[INFO] Total baris:", df.shape[0])
