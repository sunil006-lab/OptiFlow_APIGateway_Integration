#!/bin/bash

# Base paths
etcdctl put /nodes/ ""
etcdctl put /workloads/ ""
etcdctl put /mpods/ ""
etcdctl put /scheduling/ ""
etcdctl put /health/ ""
etcdctl put /config/ ""

# Nodes
etcdctl put /nodes/node-1 '{"name":"node-1", "ip":"192.168.1.10", "status":"active", "cpu":"8", "memory":"32Gi"}'
etcdctl put /nodes/node-2 '{"name":"node-2", "ip":"192.168.1.11", "status":"active", "cpu":"16", "memory":"64Gi"}'

# Workloads
etcdctl put /workloads/workload-1 '{"id":"workload-1", "node":"node-1", "image":"nginx:latest", "status":"running", "replicas":2}'
etcdctl put /workloads/workload-2 '{"id":"workload-2", "node":"node-2", "image":"redis:7", "status":"pending", "replicas":1}'

# MPODs
etcdctl put /mpods/mpod-1 '{"id":"mpod-1", "workload":"workload-1", "status":"running", "ports":[80, 443]}'
etcdctl put /mpods/mpod-2 '{"id":"mpod-2", "workload":"workload-2", "status":"initializing", "ports":[6379]}'

# Scheduling info
etcdctl put /scheduling/workload-1 '{"strategy":"spread", "node":"node-1"}'
etcdctl put /scheduling/workload-2 '{"strategy":"binpack", "node":"node-2"}'

# Health checks
etcdctl put /health/node-1 '{"cpu":15, "memory":30, "status":"healthy"}'
etcdctl put /health/node-2 '{"cpu":65, "memory":45, "status":"warning"}'

# Config
etcdctl put /config/global '{"log_level":"info", "max_retries":3, "auto_recover":true}'
etcdctl put /config/network '{"overlay":"vxlan", "service_cidr":"10.96.0.0/12"}'

