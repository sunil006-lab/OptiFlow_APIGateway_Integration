from container_wrapper import ContainerdWrapper

if __name__ == "__main__":
    cd = ContainerdWrapper(namespace="default")

    # List containers
    print("Containers:", cd.list_containers())

    # Pull image
    cd.pull_image("docker.io/library/nginx:latest")

    # Create and start a container
    cd.create_container("nginx-test", "docker.io/library/nginx:latest")
    cd.start_container("nginx-test")

    # Stop and delete container
    cd.stop_container("nginx-test")
    cd.delete_container("nginx-test")