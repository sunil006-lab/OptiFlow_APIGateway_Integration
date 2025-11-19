from container_interface import ContainerdInterface

client = ContainerdInterface()

print("🔍 Listing images:")
print(client.list_images())

print("⬇️ Pulling image:")
print(client.pull_image("docker.io/library/hello-world:latest"))

print("🚀 Running container:")
print(client.run_container("docker.io/library/hello-world:latest", "optitest"))
