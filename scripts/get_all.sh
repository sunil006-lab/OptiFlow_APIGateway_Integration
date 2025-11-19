#!/bin/bash

echo "🔍 Fetching all etcd keys and values..."

for path in /nodes/ /workloads/ /mpods/ /scheduling/ /health/ /config/
do
  echo -e "\n=== $path ==="
  etcdctl get "$path" --prefix
done

