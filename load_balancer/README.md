# Load Balancer Module - OptiFlow (AI-OrchestrateX)

The **Load Balancer** module in OptiFlow handles intelligent traffic distribution between backend services and nodes. It ensures optimal resource utilization, improves fault tolerance, and dynamically adjusts routing based on service health and load metrics.

---

## 📌 Key Responsibilities

- Distribute incoming service requests to available backend instances
- Support multiple balancing algorithms (round-robin, least connections, etc.)
- Integrate with service discovery for dynamic updates
- Monitor target service health and reroute on failure
- Interface with networking and API Gateway for request forwarding

---

## 📂 Directory Structure

| Subfolder/File        | Purpose |
|------------------------|---------|
| `algorithms/`          | Load balancing strategies and logic |
| `utils/`               | Helper functions and metrics utilities |
| `README.txt`           | Basic description (replaced by this README.md) |

---

## ⚙️ Setup Instructions

> Prerequisite: Python 3.9+, optional: Prometheus exporter (for metrics)

1. Navigate to the `load_balancer/` directory:
   ```bash
   cd load_balancer
   ```

2. Run the load balancer logic (based on your integration entry point, e.g. FastAPI/CLI/custom script):
   ```bash
   python algorithms/round_robin.py
   ```

3. Optional: Integrate with Prometheus for metrics scraping.

---

## ⚖️ Supported Algorithms

| Algorithm        | File Path                        |
|------------------|----------------------------------|
| Round Robin      | `algorithms/round_robin.py`      |
| Least Connection | `algorithms/least_conn.py`       |
| Randomized       | `algorithms/random_picker.py`    |

> These can be extended by plugging in custom strategies under `algorithms/`.

---

## 🔗 Dependencies

- Python (standard library: threading, time, random)
- Internal service registry via Orchestrator
- Optional: Prometheus/Grafana for visualizing traffic

---

## 🌐 Example Flow

1. API Gateway receives incoming traffic.
2. Forwards to Load Balancer.
3. Load Balancer chooses target node/service based on active algorithm.
4. Routes to healthy service instance dynamically.

---

## 📬 Future Enhancements

- Add feedback-aware algorithms (based on latency or success rate)
- Enable traffic shaping and rate limiting
- Build UI dashboard to monitor real-time flow

---

## 👨‍💻 Maintainers

- **Sunil Kumar M**  
  Cloud Transformation, Strategic Enablement  
  Contributor, OptiFlow (AI-OrchestrateX)

---

## 📄 License

This module is part of the OptiFlow CNCF submission. Final license and contributor agreements to be updated.

---

## 🤝 Contributions

To add a new algorithm, create a new `.py` file in `algorithms/`, follow the interface pattern, and document it. PRs are welcome once open-sourced.
