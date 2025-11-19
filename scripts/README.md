# Scripts Module - OptiFlow (AI-OrchestrateX)

The **Scripts** module contains helper scripts used for administrative tasks, data seeding, ETCD operations, table management, and automation during development, testing, and deployment phases.

---

## 📌 Key Responsibilities

- Automate ETCD population, table creation, and cleanup tasks
- Support local DB bootstrapping and schema setup
- Provide shell scripts and Python utilities for developer productivity

---

## 📂 Typical Files

| File/Script           | Purpose |
|------------------------|---------|
| `get_all.sh`           | Retrieve all ETCD key-value pairs |
| `populate_etcd.sh`     | Insert sample data into ETCD for testing |
| `create_table.py`      | Generate schema or tables for SQLite/Postgres |
| `drop_table.py`        | Cleanup tables from local DB |
| `run_project.bat`      | Windows batch to run core services |
| `testtable.py`         | Sample test cases for database logic |
| `README.txt`           | Replaced by this README.md |

---

## ⚙️ Usage Instructions

### 1. Create Tables (SQLite)
```bash
python create_table.py
