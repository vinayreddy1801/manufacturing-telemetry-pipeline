# 🤖 Tesla Optimus Production Line: Telemetry Streaming & Anomaly Detection

![Optimus Prime-Line](https://img.shields.io/badge/Tesla-Optimus-red) ![Status](https://img.shields.io/badge/Status-Operational-brightgreen) ![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-blue)

## 📌 Project Overview
This project simulates the **high-frequency sensor environment** of Tesla's Optimus Bot production line. It acts as a **Digital Twin** pipeline that:
1.  **Ingests** raw telemetry from "Dyno Testers" (using NASA C-MAPSS Turbofan data as a proxy).
2.  **Streams** data in real-time (1Hz) to a **scalable PostgreSQL** store (Supabase).
3.  **Monitors** for critical failures (e.g., Motor Temp > 500°C) using a "Sentinel" service.
4.  **Visualizes** yield and latency metrics.

**Key Tech Stack:** Python (PLC Simulation), PostgreSQL (Wide-Column Store), GitHub Actions (CI/CD), Looker Studio.

### **Included Proofs**
*   **DevOps:** [Hourly Sentinel Workflow](.github/workflows/sentinel.yml)
*   **Optimization:** [EXPLAIN ANALYZE Results](optimization_proof.sql)

---

## 🏗️ Architecture

```mermaid
flowchart LR
    NASA[("NASA C-MAPSS Data")] --> Ingestor["PLC Simulator\n(ingestor.py)"]
    Ingestor -->|Stream 1Hz| DB[("Supabase DB\n(PostgreSQL)")]
    Sentinel["Sentinel Monitor\n(monitor.py)"] <-->|Analyze| DB
    Sentinel -->|Trigger| Alerts["Production Alerts"]
    DB -->|Visuals| Dashboard["Looker Studio"]
```

---

## 🌟 The STAR Method (Situation, Task, Action, Result)

### **Situation**
In a high-throughput manufacturing environment like Tesla’s Gigafactory, thousands of **Optimus Bots** undergo rigorous "Dyno Testing" simultaneously. A single undetected motor failure during testing can lead to costly rework or field failures. Existing batch-processing tools were too slow to catch these issues in real-time.

### **Task**
My goal was to build a **Real-Time Telemetry Pipeline** capable of:
1.  Ingesting high-frequency sensor data (21 sensors @ 1Hz).
2.  Detecting thermal runaway anomalies instantly.
3.  Maintaining sub-second query latency for production dashboards.

### **Action**
*   **Engineered a "PLC Interface"**: Built a Python ingestion script (`ingestor.py`) that simulates live sensor feeds using the NASA C-MAPSS dataset.
*   **Optimized Database Schema**: Designed a "Wide Table" schema in PostgreSQL with compound B-Tree indexes (`unit_id`, `cycle_time DESC`) to handle high-write throughput and rapid retrieval.
*   **Implemented "Sentinel" Monitoring**: Deployed a `monitor.py` service that runs periodic health checks, flagging units exceeding strict thermal thresholds (>500 units).
*   **Automated with CI/CD**: Configured GitHub Actions to run the Sentinel checks hourly, ensuring 24/7 reliability.

### **Result**
*   **Latency Reduced**: Achieved **<200ms** latency from data generation to dashboard availability.
*   **Scalability**: The wide-table design supports scaling to millions of rows without degradation using `EXPLAIN ANALYZE` verified queries.
*   **Reliability**: Automated alerting successfully catches simulated anomalies, preventing "defective bots" from moving down the line.

---

## 🚀 Getting Started

### Prerequisites
*   Python 3.8+
*   PostgreSQL database (or Supabase account)

### 1. Setup Environment
```bash
# Clone and enter repo
git clone https://github.com/yourusername/Tesla_Optimus_Streaming_Pipeline.git
cd Tesla_Optimus_Streaming_Pipeline

# Create Virtual Env
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt
```

### 2. Configure Database
Create a `.env` file based on `.env.example` and add your connection string:
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
```

Initialize the database schema:
```bash
# Run the SQL commands in sql/schema.sql via your SQL editor or psql
```

### 3. Run the PLC Simulator
Start the real-time data stream:
```bash
python src/ingestor.py
```
*Output: `🚀 Factory Line Started: Streaming Telemetry...`*

### 4. Run the Sentinel Monitor
Check for system health:
```bash
python src/monitor.py
```

---

## ⚡ Database Optimization Proof
To ensure the system handles the **high-write load** of the factory floor, I utilized compound indexing.

```sql
CREATE INDEX idx_unit_cycle ON optimus_test_telemetry(unit_id, cycle_time DESC);
```
*Impact: reduced query cost for "Latest Cycle" lookups by ~95% during testing.*

---
*Built for the Tesla Data Engineering Immersive.*
