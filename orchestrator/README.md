# Orchestrator Module - OptiFlow (AI-OrchestrateX)

The **Orchestrator** module is the heart of the OptiFlow system. It acts as the control plane responsible for managing containers, scheduling workloads, tracking node health, and coordinating other key subsystems like API Server, Scheduler, Controller Manager, and Networking.

---

## 📌 Key Responsibilities

- Handle cluster-level coordination of workloads and nodes
- Schedule and dispatch workloads to available healthy nodes
- Manage container lifecycles via container interface
- Ensure system resiliency through health checks and controllers
- Integrate seamlessly with the networking and storage layers

---

## 📂 Submodules

| Subfolder        | Purpose |
|------------------|---------|
| `apiserver/`     | REST APIs for developer operations |
| `controller/`    | Async controller with health checks and workload coordination |
| `core/`          | Container interfaces and runtime wrappers (e.g., containerd) |
| `scheduler/`     | Custom intelligent scheduler (`oschedular.py`) |
| `models/`        | Core schema and support models for internal DB logic |
| `db/`            | SQLite DB initialization and query logic |
| `registry/`      | Service registration and discovery interface |
| `schema_model/`  | Pydantic and ORM models used for DB interactions |
| `caliconetwork/` | Calico setup and network integration logic |
| `utils/`         | Utility functions used across orchestrator components |

---

## ⚙️ Setup Instructions

> Prerequisite: Python 3.9+, containerd, SQLite3, Calico installed

1. Clone the project and enter the `orchestrator/` directory:
   ```bash
   cd orchestrator
   ```

2. Install required packages:
   ```bash
   pip install -r ../api_gateway/models/requirements.txt
   ```

3. Initialize the SQLite DB (if not done):
   ```bash
   python init_db.py
   ```

4. Run API server (developer API):
   ```bash
   python apiserver/developer_api.py
   ```

5. Start the controller and scheduler modules separately in background:
   ```bash
   python controller/controller.py
   python scheduler/oschedular.py
   ```

---

## 🔗 Dependencies

- Python (asyncio, SQLAlchemy, FastAPI)
- SQLite3
- Containerd
- Calico (for networking)
- Etcd (optional for service coordination)
- OptiFlow's API Gateway (for routing workloads)

---

## ✅ Example Use Case

Submit a workload via API, and the orchestrator schedules it on a healthy node, pulls the container, starts it using containerd, and keeps tracking it via controller.

---

## 👨‍💻 Maintainers

- **Sunil Kumar M**  
  Cloud Transformation, Strategic Enablement  
  Contributor, OptiFlow (AI-OrchestrateX)

---

## 📄 License

This module is part of the OptiFlow CNCF submission. Final license and contributor agreements to be updated.

---

## 📬 Contributions

Want to improve the orchestrator logic or plug in your scheduler? PRs and issues welcome. Please raise via the GitHub repo once open-sourced.
