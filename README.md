<img width="1216" height="558" alt="WhatsApp Image 2025-11-25 at 23 50 14_d5a4c214" src="https://github.com/user-attachments/assets/b0fbebf0-8b6e-42a8-b960-b6a24d89c6ea" />


https://github.com/user-attachments/assets/b699ddbb-0d9c-4dba-9a5e-8a9b1e838560

# 🛡️ Enterprise Production Log Anomaly Radar & Alerting System

An end-to-end, memory-optimized streaming telemetry dashboard designed to ingest production server transaction logs, run live feature extraction, and leverage an unsupervised **Isolation Forest** machine learning algorithm to intercept and isolate security anomalies in real-time.

---

## 🚀 Key Architectural Features
* **Streaming Architecture:** Uses lazy chunk-loading arrays via Pandas to ingest mass raw transactional inputs row-by-row with minimal overhead, simulating a true streaming telemetry line.
* **Defensive Engineering Block:** Outfitted with robust `try-except` execution checkpoints to catch, log, and skip malformed or corrupt numerical payloads without interrupting the live visualization stream.
* **Persistent Session State Memory:** Leverages custom state tokens to prevent data volatility, ensuring metrics, charts, and audit logs remain fully visible on the user interface even after the data stream finishes or halts.
* **Incident Audit Exporter:** Features a one-click dynamic forensic reporting module to package and download captured infrastructure anomalies directly into standard `.csv` spreads for automated incident distribution.

---

## 🛠️ Technological Infrastructure Stack
* **Frontend UI Framework:** Streamlit (Custom Dark Matrix CSS Styling overrides)
* **Core Analytics Platform:** Pandas, NumPy
* **Machine Learning Intelligence Core:** Scikit-Learn (Unsupervised Outlier Isolation Model Core)
* **State Compression Serialization:** Joblib

---

## ⚡ Setup & Production Replication Guide

To replicate, evaluate, or scale this monitoring infrastructure locally on your machine, follow these configurations:

### 1. Initialize Project Directory & Dependencies
Clone or download this repository, navigate into the core project folder using your terminal interface, and install the required environment manifest:
```bash
pip install -r requirements.txt

# 🛡️ Enterprise Production Log Anomaly Radar & Alerting System

A real-time, end-to-end telemetry surveillance pipeline that ingests simulated system logs, evaluates payload features using an unsupervised **Isolation Forest** Machine Learning model, and automatically dispatches automated breach alerts to a **Discord Security Operations (SecOps)** channel when anomaly thresholds are violated.

🚀 **Live Production Link:** [https://log-anomaly-detector-fkihaappnvumqj6wxsw7hd7.streamlit.app/]

---

## 📈 System Architecture & Flow
<img width="800" height="379" alt="ezgif-499a5a852900e2e0" src="https://github.com/user-attachments/assets/2fa23a67-ab2d-4e2e-a3c4-232702b3f87e" />

1. **Telemetry Data Stream:** Ingests live production server logs sequentially via a custom Pandas chunking engine.
2. **Defensive Preprocessing Block:** Sanitizes missing metrics, calculates dynamic operational engagement factors, and catches malformed network payloads safely.
3. **Machine Learning Core:** Leverages an unsupervised Isolation Forest model to detect feature anomalies and malicious traffic spikes.
4. **Automated Incident Response Wrapper:** Serializes data metrics dynamically and ships webhook payloads directly to an external API (Discord) upon threshold breach.

---

## 🛠️ Tech Stack & Tooling

* **Language:** Python 3.x
* **Framework:** Streamlit (Dynamic Live UI Dashboard)
* **Machine Learning:** Scikit-Learn (Isolation Forest Outlier Detection)
* **Serialization & Analytics:** Pandas, Joblib, JSON
* **Alerting Protocol:** Discord Webhook REST API Integration via `requests`

---

## ⚙️ Core Engineering Features

* **Real-Time Data Ingestion:** Processes simulated system activity seamlessly with adjustable telemetry speeds.
* **Granular Controls:** Dynamic sidebar options to adjust outlier contamination levels and alert tripwire sensitivities on the fly.
* **Audit Trail Export:** Generates an on-demand, down-loadable incident log CSV for post-breach forensic analysis.
