from grpc import metadata_call_credentials

class ContainerdManager:
    def __init__(self, socket_path="unix:///run/containerd/containerd.sock", namespace="default"):
        print("Inside init fun")
        self.namespace = namespace
        self.channel = grpc.insecure_channel(socket_path)
        self.client = containers_pb2_grpc.ContainersStub(self.channel)

    def list_containers(self):
        print("Inside list container fun")
        request = containers_pb2.ListContainersRequest()
        metadata = [("containerd-namespace", self.namespace)]
        response = self.client.List(request, metadata=metadata)
        for c in response.containers:
            print(f"Container ID: {c.id}")