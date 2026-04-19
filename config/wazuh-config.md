# 🔧 Wazuh Configuration Overview

This document describes the configuration and architecture of the Wazuh-based SIEM system used in this project.

---

## 🏗️ System Architecture

The system is deployed on AWS EC2 using a multi-instance architecture:

* **Wazuh Manager** → Central analysis & rule engine
* **Wazuh Agent (Web Server)** → Log collection
* **Elasticsearch** → Log storage & indexing
* **Machine Learning Engine** → Anomaly detection (Random Forest)

---

## 🌐 Network Configuration

All instances are deployed within the same VPC and communicate through private IP.

### Open Ports

| Port | Service            | Description                 |
| ---- | ------------------ | --------------------------- |
| 22   | SSH                | Remote access to servers    |
| 80   | HTTP               | Web server access           |
| 443  | HTTPS              | Secure web access           |
| 1514 | Wazuh Agent        | Log communication (TCP/UDP) |
| 1515 | Wazuh Registration | Agent registration          |
| 9200 | Elasticsearch      | REST API access             |
| 5601 | Kibana             | Log visualization dashboard |

---

## ⚙️ Wazuh Manager Configuration

### Key Functions:

* Log analysis (decoder + rules)
* Threat detection (rule-based)
* Alert generation

### Important Files:

```bash
/var/ossec/etc/ossec.conf
/var/ossec/logs/alerts/alerts.json
```

### Agent Connection:

* Agents send logs to Manager via port **1514**
* Agent registration via port **1515**

---

## 🖥️ Wazuh Agent Configuration

Installed on the web server (Ubuntu 22.04)

### Monitored Logs:

```bash
/var/log/auth.log
/var/log/syslog
/var/log/apache2/access.log
```

### Agent Configuration File:

```bash
/var/ossec/etc/ossec.conf
```

---

## 📦 Elasticsearch Configuration

Elasticsearch is used to store and index logs from Wazuh.

### Key Features:

* JSON-based log storage
* Fast querying via REST API
* Data indexing for analytics

### Example Index:

```bash
wazuh-alerts-*
```

### API Access:

```bash
http://<ELASTIC_IP>:9200
```

---

## 📊 Kibana Dashboard

Kibana is used for visualization and log analysis.

### Features:

* Real-time monitoring
* Search & filtering logs
* Dashboard visualization

### Access:

```bash
http://<ELASTIC_IP>:5601
```

---

## 🤖 Machine Learning Integration

The Machine Learning engine is deployed separately and works as an additional analysis layer.

### Workflow:

1. Fetch logs from Elasticsearch (REST API)
2. Preprocess data
3. Apply Random Forest model
4. Classify:

   * 0 → Normal
   * 1 → Anomaly
5. Send alert if anomaly detected

---

## 🔔 Alerting System (Telegram)

When anomaly is detected:

* System sends notification via Telegram Bot API

### Alert contains:

* Timestamp
* IP Address
* Event Type
* Severity

---

## 🔐 Security Considerations

* Use Security Groups to restrict access
* Only necessary ports are opened
* SSH access should be limited (recommended: key-based only)
* Sensitive data should not be stored in repository

---

## 📌 Notes

* Wazuh performs rule-based detection
* Machine Learning adds behavioral anomaly detection
* Combination improves detection accuracy and reduces false positives

---
