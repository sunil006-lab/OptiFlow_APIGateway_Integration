# Networking Module - OptiFlow (AI-OrchestrateX)

The **Networking** module is responsible for inter-service communication, service discovery, and routing inside the OptiFlow cluster. It provides foundational networking infrastructure such as service-to-service routing, DNS resolution, and gateway exposure.

---

## 📌 Key Responsibilities

- Enable communication across all microservices and nodes
- Route requests using in-cluster and external gateways
- Perform service discovery via custom or external registry
- Integrate with Calico or other CNI plugins for network policy enforcement

---

## 📂 Directory Structure

| Subfolder          | Purpose |
|---------------------|---------|
| `gateway/`          | Handles north-south traffic (external to internal) |
| `load_balancer/`    | Internal layer-7 routing logic (can extend main load balancer) |
| `service_discovery/`| Discovery logic and DNS mappings between services |
| `README.txt`        | Description (replaced by this README.md) |

---

## 🌐 Functional Scope

- **East-West Routing**: Between services via service discovery layer  
- **North-South Routing**: From clients to internal services via gateway  
- **Dynamic Discovery**: Works with Orchestrator's registry to locate services  
- **Security**: Future support for network policies via Calico and TLS mesh

---

## ⚙️ Setup Instructions

> Prerequisite: Python 3.9+, running orchestrator and service registry

1. Navigate to networking module:
   ```bash
   cd networking
