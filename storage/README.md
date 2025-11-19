# Storage Module - OptiFlow (AI-OrchestrateX)

The **Storage** module provides persistent data storage support for the OptiFlow platform. It includes multiple backend implementations like SQLite, Redis, and PostgreSQL to support workload metadata, configuration, state management, and real-time processing.

---

## 📌 Key Responsibilities

- Store container and workload metadata
- Enable state management for orchestration flows
- Support fast caching for controller/scheduler using Redis
- Provide persistent DB options for production and local dev

---

## 📂 Directory Structure

| Subfolder/File     | Purpose |
|---------------------|---------|
| `sqlite/`           | Lightweight embedded storage for local testing |
| `postgres/`         | Production-grade SQL database support |
| `redis/`            | In-memory DB for caching, message queues, state tracking |
| `test_data/`        | Sample datasets for dev/testing |
| `README.txt`        | Replaced by this README.md |

---

## 💾 Supported Storage Backends

| Backend     | Use Case |
|-------------|----------|
| SQLite      | Local development, prototyping |
| PostgreSQL  | Production deployment (centralized DB) |
| Redis       | Fast caching, pub-sub, heartbeat tracking |

---

## ⚙️ Setup Instructions

### For SQLite:
1. Auto-initialized via orchestrator:
   ```bash
   python orchestrator/init_db.py
