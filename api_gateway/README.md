# API Gateway Module - OptiFlow (AI-OrchestrateX)

The **API Gateway** module is the primary entry point for all external and internal client requests in OptiFlow. It performs intelligent routing, request transformation, authentication, and forwarding to appropriate backend services like orchestrator, AI agents, and frontend.

---

## 📌 Key Responsibilities

- Expose unified entry points for APIs (RESTful)
- Route requests based on service discovery or internal logic
- Authenticate and authorize consumers via middleware
- Support load balancing and failover across backend services
- Integrate AI inference and prediction endpoints seamlessly

---

## 📂 Directory Structure

| Subfolder/File               | Purpose |
|-----------------------------|---------|
| `api_gateway_entry.py`      | Main FastAPI application runner |
| `consumer-test.py`          | Local test client for simulating API calls |
| `server_config.env`         | Environment configurations (ports, tokens) |
| `routers/`                  | Defines route mappings for API endpoints |
| `services/`                 | Core business logic and auth middleware |
| `models/`                   | Pre-trained ML models and model driver code |
| `utils/`                    | Utilities and helper functions |
| `README.txt`                | Description (replaced by this README.md) |

---

## ⚙️ Setup Instructions

> Prerequisite: Python 3.9+, FastAPI, Uvicorn, PyTorch (for ML models)

1. Navigate to the `api_gateway/` directory:
   ```bash
   cd api_gateway
   ```

2. Install required packages:
   ```bash
   pip install -r models/requirements.txt
   ```

3. Start the API Gateway:
   ```bash
   uvicorn api_gateway_entry:app --host 0.0.0.0 --port 8000
   ```

4. Optional: Run the consumer test to verify routing:
   ```bash
   python consumer-test.py
   ```

---

## 🔐 Authentication & Middleware

The `auth_middleware.py` file under `services/` handles basic token-based auth. The `server_config.env` file stores shared tokens used by internal services or consumers.

---

## 🧠 Model Integration

Pre-trained PyTorch models (e.g., `best_payment_order_model.pth`) are loaded via `payment_order_model_main.py` and used in response to relevant API calls (e.g., payment predictions).

---

## 🌐 Example API Endpoints

| Method | Endpoint                  | Description                      |
|--------|---------------------------|----------------------------------|
| GET    | `/api/predict/payment`    | Predicts payment order outcome   |
| POST   | `/api/route/service`      | Routes request to orchestrator   |
| GET    | `/api/health`             | Gateway health check             |

---

## 🔗 Dependencies

- FastAPI
- Uvicorn
- PyTorch
- Requests
- OS/ENV packages

---

## 🧪 Testing

Tests are provided in `tests/api_tests/` directory (e.g., `testapigw.py`, `test_api_gateway.ipynb`).  
Ensure gateway is running before executing tests.

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

Have an idea to improve routing or add observability middleware? PRs are welcome. Please fork and raise via GitHub once public.
