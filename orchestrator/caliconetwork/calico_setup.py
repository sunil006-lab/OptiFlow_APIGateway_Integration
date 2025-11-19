import os
import subprocess

CNI_BIN_DIR = "/opt/cni/bin"
CNI_CONF_DIR = "/etc/cni/net.d"
CALICO_VERSION = "v3.27.0"

def download_calico_binaries():
    """
    Pulls Calico CNI plugin image using full qualified name and extracts binaries from it.
    """
    img = "docker.io/calico/cni:v3.30.2"
    os.makedirs(CNI_BIN_DIR, exist_ok=True)

    # Pull image
    subprocess.run(["ctr", "image", "pull", "--plain-http=false", img], check=True)

    # Create a container to extract binaries
    subprocess.run([
        "ctr", "run", "--rm", "--mount", f"type=bind,src={CNI_BIN_DIR},dst=/out",
        img, "extract-cni",
        "tar", "-C", "/out", "-xzvf", "/opt/cni/bin/cni-amd64.tgz"
    ], check=True)

    print("Calico CNI binaries extracted successfully to /opt/cni/bin.")




def write_calico_cni_config():
    """
    Writes the Calico CNI network configuration file (for etcd mode).
    """
    config = """
{
  "cniVersion": "0.3.1",
  "name": "calico",
  "plugins": [
    {
      "type": "calico",
      "log_level": "info",
      "datastore_type": "etcd",
      "etcd_endpoints": "http://127.0.0.1:2379",
      "nodename": "optiflow-node",
      "ipam": {
        "type": "calico-ipam"
      },
      "policy": {
        "type": "none"
      }
    },
    {
      "type": "portmap",
      "snat": true,
      "capabilities": {
        "portMappings": true
      }
    }
  ]
}
"""
    os.makedirs(CNI_CONF_DIR, exist_ok=True)
    with open(os.path.join(CNI_CONF_DIR, "10-calico.conflist"), "w") as f:
        f.write(config)
    print("Calico CNI configuration written to 10-calico.conflist.")

if __name__ == "__main__":
    download_calico_binaries()
    write_calico_cni_config()
