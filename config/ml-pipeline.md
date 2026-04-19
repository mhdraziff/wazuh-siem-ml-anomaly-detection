# 🤖 Machine Learning Pipeline (Anomaly Detection)

This document describes the machine learning workflow used to detect anomalies in system logs.

---

## 🎯 Objective

To classify log events into:

* **0 → Normal**
* **1 → Anomaly**

The model is used as an additional detection layer on top of Wazuh SIEM.

---

## 🧩 Pipeline Overview

```
Log Data (Elasticsearch)
        ↓
Data Collection (Python Script)
        ↓
Preprocessing & Feature Engineering
        ↓
Model Training (Random Forest)
        ↓
Evaluation (Confusion Matrix)
        ↓
Real-time Detection
        ↓
Telegram Alert
```

---

## 📥 1. Data Collection

Logs are retrieved from Elasticsearch using REST API.

### Source Index:

```bash id="ml1"
wazuh-alerts-*
```

### Example Fields:

* timestamp
* rule.level
* rule.firedtimes
* agent.name
* full_log

### Script:

```bash id="ml2"
scripts/data_collection.py
```

---

## 🧹 2. Preprocessing

Raw log data is cleaned and transformed into structured format.

### Steps:

* Remove unnecessary fields
* Handle missing values
* Normalize data format
* Convert timestamp to hour

### Script:

```bash id="ml3"
scripts/preprocessing.py
```

---

## 🧠 3. Feature Engineering

New features are created to improve model performance.

### Features Used:

* **firedtimes** → frequency of alert
* **rule_level** → severity level
* **hour** → time of event
* **is_night** → 1 if event occurs between 00:00–05:00
* **is_ssh** → 1 if log relates to SSH activity
* **log_length** → length of log message

These features help the model identify abnormal patterns.

---

## 🏋️ 4. Model Training

### Algorithm:

Random Forest (Supervised Learning)

### Reason:

* Handles complex patterns
* Reduces overfitting
* Works well with structured log data

### Process:

* Split dataset (train/test)
* Train multiple decision trees
* Use majority voting for classification

### Script:

```bash id="ml4"
scripts/train_model.py
```

---

## 📊 5. Model Evaluation

Model performance is evaluated using confusion matrix.

### Metrics:

* Accuracy
* Precision
* Recall
* F1-Score

### Important:

Recall is prioritized because:

* False Negative = undetected attack (high risk)

### Script:

```bash id="ml5"
scripts/evaluate.py
```

---

## ⚡ 6. Real-Time Detection

After training, the model is used for real-time anomaly detection.

### Workflow:

1. Fetch new logs from Elasticsearch
2. Apply preprocessing
3. Predict using trained model
4. If anomaly detected → trigger alert

### Script:

```bash id="ml6"
scripts/detection.py
```

---

## 🔔 7. Alerting (Telegram)

If anomaly is detected:

* System sends notification using Telegram Bot API

### Alert Example:

* Timestamp
* Source IP
* Event type
* Severity level

---

## 📦 Model Storage

The trained model is saved using:

```bash id="ml7"
model/random_forest_model.pkl
```

Used for:

* Reuse without retraining
* Faster inference

---

## ⚠️ Limitations

* Dataset based on simulated attacks
* No hyperparameter tuning (basic implementation)
* Limited to Random Forest (no deep learning)

---

## 🚀 Future Improvements

* Add anomaly detection (unsupervised learning)
* Hyperparameter tuning
* Integrate with real SOC environments
* Improve dataset diversity

---

## 📌 Summary

This pipeline enhances traditional SIEM by:

* Adding behavioral analysis
* Reducing false positives
* Detecting unseen attack patterns

---
