# Tests Module - OptiFlow (AI-OrchestrateX)

The **Tests** module includes unit, integration, and functional test suites for validating the behavior and reliability of all OptiFlow components. Each major subsystem (API Gateway, Orchestrator, Agents, Frontend) has its own test folder and automation logic.

---

## 📌 Key Responsibilities

- Validate correctness of service routing and orchestration logic
- Ensure model predictions meet expected accuracy and latency
- Perform load and stress testing of core modules
- Automate CI pipelines for CNCF readiness

---

## 📂 Directory Structure

| Folder                  | Purpose |
|--------------------------|---------|
| `agents_tests/`          | Tests for AI agents and model outputs |
| `api_tests/`             | API Gateway test cases and Jupyter test flows |
| `frontend_tests/`        | UI-level tests for web dashboard and components |
| `load_tests/`            | Load/stress simulations across orchestrator and gateway |
| `orchestrator_tests/`    | Scheduler, controller, and registry unit tests |
| `test_data/`             | Sample data inputs and expected outputs |
| `README.txt`             | Replaced by this README.md |

---

## 🧪 Sample Test Coverage

- API endpoint verification using `testapigw.py`
- Orchestrator scheduling logic validation (mock nodes & workloads)
- Medical agent testing with image inputs in `.npy` format
- Load simulation using concurrent workload submissions

---

## ⚙️ Setup Instructions

> Prerequisite: Python 3.9+, pytest, requests, unittest, Jupyter (for `.ipynb`)

1. Install dependencies:
   ```bash
   pip install pytest requests
