import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from konfigurasi import FILE_CLEAN, FILE_MODEL
def latih_model():
df = pd.read_csv(FILE_CLEAN)
print(f"[INFO] Membaca dataset clean: {FILE_CLEAN}")
print("[INFO] Total baris:", df.shape[0])
X = df.drop(columns=["label"])
y = df["label"]
strat = y if y.nunique() > 1 else None
X_train, X_test, y_train, y_test = train_test_split(
X, y, test_size=0.3, random_state=42, stratify=strat
)
print("[INFO] Data training:", X_train.shape[0])
print("[INFO] Data testing :", X_test.shape[0])
print("[INFO] Melatih model Random Forest...")
model = RandomForestClassifier(
n_estimators=300,
random_state=42,
class_weight="balanced"
)
model.fit(X_train, y_train)
joblib.dump(model, FILE_MODEL)
print(f"✅ Model berhasil disimpan: {FILE_MODEL}")
if __name__ == "__main__":
latih_model()
