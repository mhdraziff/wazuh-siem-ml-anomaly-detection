import time
import requests
import pandas as pd
import joblib
from konfigurasi import ELASTIC_BASE_URL, INDEX_PATTERN,
FILE_MODEL
def ambil_alert_terbaru():
url = f"{ELASTIC_BASE_URL}/{INDEX_PATTERN}/_search"
query = {
"size": 1,
"sort": [{"@timestamp": {"order": "desc"}}],
"query": {"match_all": {}}
}
resp = requests.get(url, json=query, timeout=30)
if resp.status_code != 200:
print("[ERROR] Gagal ambil alert terbaru:",
resp.status_code, resp.text[:200])
return None
data = resp.json()
hits = data.get("hits", {}).get("hits", [])
if not hits:
return None
return hits[0].get("_source", {})
def ekstrak_fitur(src):
rule_level = src.get("rule", {}).get("level", 0)
firedtimes = src.get("rule", {}).get("firedtimes", 1)
rule_desc = src.get("rule", {}).get("description", "")
full_log = src.get("full_log", "")
ts = src.get("@timestamp", "")
ts_dt = pd.to_datetime(ts, errors="coerce", utc=True)
hour = int(ts_dt.hour) if pd.notna(ts_dt) else 0
is_night = 1 if 0 <= hour <= 5 else 0
log_length = len(str(full_log))
is_ssh = 1 if ("ssh" in str(rule_desc).lower() or "sshd"
in str(full_log).lower()) else 0
fitur = {
"firedtimes": int(firedtimes) if
str(firedtimes).isdigit() else 1,
"rule_level": int(rule_level) if
str(rule_level).isdigit() else 0,
"hour": hour,
"is_night": is_night,
"is_ssh": is_ssh,
"log_length": log_length
}
return fitur, ts, rule_desc
def realtime_loop(interval=20):
model = joblib.load(FILE_MODEL)
last_ts = None
print("[INFO] Realtime detector aktif...")
print("[INFO] Model:", FILE_MODEL)
print("[INFO] Interval:", interval, "detik\n")
while True:
src = ambil_alert_terbaru()
if src is None:
print("[INFO] Belum ada alert terbaru.")
time.sleep(interval)
continue
ts = src.get("@timestamp", "")
if not ts or ts == last_ts:
time.sleep(interval)
continue
last_ts = ts
fitur, ts, rule_desc = ekstrak_fitur(src)
X = pd.DataFrame([fitur])
pred = int(model.predict(X)[0])
agent = src.get("agent", {}).get("name", "")
level = src.get("rule", {}).get("level", 0)
ft = src.get("rule", {}).get("firedtimes", 1)
full_log = src.get("full_log", "")
print("\n==============================")
print("[BUKTI 1] Alert terbaru berhasil diambil dari
Elasticsearch")
print("Waktuprint("\n[BUKTI 4] Potongan full_log:")
print(str(full_log)[:200], "...")
print("==============================\n")
time.sleep(interval)
if __name__ == "__main__":
realtime_loop(interval=20)
:", ts)
print("Agent
:", agent)
print("Rule Level :", level, "| Firedtimes:", ft)
print("Rule Desc :", rule_desc)
print("\n[BUKTI 2] Fitur hasil preprocessing (input
ke ML):")
print(fitur)
print("\n[BUKTI 3] Hasil prediksi ML (1=anomali,
0=normal):", pred)

