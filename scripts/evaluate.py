import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,
confusion_matrix
from konfigurasi import FILE_CLEAN, FILE_MODEL, FILE_REPORT,
FILE_CONFUSION
def evaluasi_model():
df = pd.read_csv(FILE_CLEAN)
print(f"[INFO] Membaca dataset clean: {FILE_CLEAN}")
print("[INFO] Total baris:", df.shape[0])
X = df.drop(columns=["label"])
y = df["label"]
strat = y if y.nunique() > 1 else None
X_train, X_test, y_train, y_test = train_test_split(
X, y, test_size=0.3, random_state=42, stratify=strat
)
model = joblib.load(FILE_MODEL)
print(f"[INFO] Model dimuat: {FILE_MODEL}")
y_pred = model.predict(X_test)
report = classification_report(y_test, y_pred, digits=4)
cm = confusion_matrix(y_test, y_pred)
print("\n=== Classification Report ===")
print(report)
print("=== Confusion Matrix ===")
print(cm)
# Simpan classification report
with open(FILE_REPORT, "w", encoding="utf-8") as f:
f.write("Classification Report\n")
f.write(report + "\n")
# Simpan confusion matrix ke CSV
cm_df = pd.DataFrame(cm, index=["aktual_0", "aktual_1"],
columns=["prediksi_0", "prediksi_1"])
cm_df.to_csv(FILE_CONFUSION, index=True)
print(f"\n✅ Report disimpan: {FILE_REPORT}")
print(f"✅ Confusion matrix disimpan:
{FILE_CONFUSION}")
if __name__ == "__main__":
evaluasi_model()
