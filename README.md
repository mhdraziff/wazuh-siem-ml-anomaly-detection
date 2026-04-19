# 🔐 SIEM + Machine Learning for Anomaly Detection (Wazuh)

## 🚨 Problem

Traditional SIEM systems like Wazuh rely on **rule-based detection**, which:

* Cannot detect unknown attack patterns
* Generates high false positives
* Requires manual analysis

---

## 💡 Solution

This project enhances SIEM by integrating **Machine Learning (Random Forest)** to:

* Classify logs into **normal vs anomaly**
* Reduce false positives
* Add intelligent detection layer

---

## 🏗️ Architecture

![Topology](docs/topology.png)

---

## 🔄 Workflow

![Flowchart](docs/flowchart.png)

---

## ⚙️ How It Works

1. Web server generates logs (SSH, Apache, system logs)
2. Wazuh Agent sends logs to Wazuh Manager
3. Logs stored in Elasticsearch
4. Machine Learning Engine:

   * Fetch logs via API
   * Preprocess data
   * Classify using Random Forest
5. If anomaly detected → Telegram alert sent

---

## 🧠 Machine Learning Details

* Algorithm: Random Forest
* Type: Supervised Learning
* Features:

  * firedtimes
  * rule_level
  * hour
  * is_night
  * is_ssh
  * log_length

---

## 📊 Results

### Confusion Matrix

![CM](screenshots/confusion-matrix.png)

### Key Insight

* ML improves anomaly classification accuracy
* Reduces false positive alerts
* Adds intelligent validation layer on top of Wazuh

---

## 📸 System Output

### Wazuh Alerts

![Wazuh](screenshots/wazuh-dashboard.png)

### Kibana Monitoring

![Kibana](screenshots/kibana.png)

### Telegram Alert

![Telegram](screenshots/telegram-alert.png)

---

## 🛠️ Tech Stack

* Wazuh (SIEM)
* Elasticsearch + Kibana
* AWS EC2
* Python (Scikit-learn, Pandas)
* Telegram Bot API

---

## 📂 Key Components

```bash id="struct1"
scripts/
  ├── data_collection.py
  ├── preprocessing.py
  ├── train_model.py
  ├── evaluate.py
  └── detection.py
```

---

## 🎯 Why This Project Matters

This project simulates a **real SOC environment** by:

* Monitoring logs in real-time
* Detecting attacks (brute force, scanning, file change)
* Automating alerting system

---

## 👨‍💻 Author

Muhammad Razif
Aspiring SOC Analyst | Cybersecurity Enthusiast
