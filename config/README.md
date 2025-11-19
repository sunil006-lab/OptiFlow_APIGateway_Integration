# Config Module - OptiFlow (AI-OrchestrateX)

The **Config** module manages centralized configuration and secrets for all OptiFlow components. It ensures secure, environment-specific, and structured access to required runtime variables such as service ports, DB credentials, and feature toggles.

---

## 📌 Key Responsibilities

- Store environment-level variables (dev, stage, prod)
- Centralize secrets in a structured directory hierarchy
- Enable secure loading of runtime parameters for API Gateway, Orchestrator, Load Balancer, etc.
- Simplify deployment configuration across multiple environments

---

## 📂 Directory Structure

| Folder/File              | Purpose |
|---------------------------|---------|
| `env/`                    | All environment-specific config folders |
| `env/secrets/dev/`        | Development environment secrets |
| `env/secrets/stage/`      | Staging environment secrets |
| `env/secrets/prod/`       | Production environment secrets |
| `README.txt`              | Replaced by this README.md |

---

## 🔐 Example Environment Files

A `.env` file (or `.json`/`.yaml`) in each secret directory may include:
```dotenv
API_GATEWAY_PORT=8000
DATABASE_URL=sqlite:///orchestrator.db
REDIS_HOST=localhost
AUTH_TOKEN=supersecret123
