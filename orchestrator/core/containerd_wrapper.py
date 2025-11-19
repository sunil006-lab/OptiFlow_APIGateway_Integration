import grpc
import time
from google.protobuf import empty_pb2

# Import generated gRPC classes
from services.containers.v1 import containers_pb2_grpc, containers_pb2
from services.tasks.v1 import tasks_pb2_grpc, tasks_pb2
from services.images.v1 import images_pb2_grpc, images_pb2

class ContainerdWrapper:
    def __init__(self, socket_path="unix:///run/containerd/containerd.sock", namespace="default"):
        self.namespace = namespace
        self.channel = grpc.insecure_channel(socket_path)
        self.container_stub = containers_pb2_grpc.ContainersStub(self.channel)
        self.task_stub = tasks_pb2_grpc.TasksStub(self.channel)
        self.image_stub = images_pb2_grpc.ImagesStub(self.channel)

    def _metadata(self):
        return [("containerd-namespace", self.namespace)]

    def list_containers(self):
        request = containers_pb2.ListContainersRequest()
        response = self.container_stub.List(request, metadata=self._metadata())
        return [c.id for c in response.containers]

    def pull_image(self, image_name):
        print(f"Pulling image: {image_name}")
        request = images_pb2.PullImageRequest(
            image=image_name,
            schema1=True  # compatibility
        )
        self.image_stub.Pull(request, metadata=self._metadata())
        print(f"Image '{image_name}' pulled successfully.")
        
    def create_container(self, container_id, image_name):
        container = containers_pb2.Container(
            id=container_id,
            image=image_name,
            runtime=containers_pb2.Container.Runtime(name="io.containerd.runc.v2")
        )
        self.container_stub.Create(
            containers_pb2.CreateContainerRequest(container=container),
            metadata=self._metadata()
        )
        print(f"Container '{container_id}' created.")

    def start_container(self, container_id):
        task_request = tasks_pb2.CreateTaskRequest(container_id=container_id)
        self.task_stub.Create(task_request, metadata=self._metadata())
        self.task_stub.Start(tasks_pb2.StartRequest(container_id=container_id), metadata=self._metadata())
        print(f"Container '{container_id}' started.")

    def stop_container(self, container_id):
        print(f"Stopping container '{container_id}'...")
        self.task_stub.Kill(tasks_pb2.KillRequest(container_id=container_id, signal=15), metadata=self._metadata())
        time.sleep(2)  # Give it a moment to stop
        self.task_stub.Delete(tasks_pb2.DeleteTaskRequest(container_id=container_id), metadata=self._metadata())
        print(f"Container '{container_id}' stopped and deleted.")

    def delete_container(self, container_id):
        self.container_stub.Delete(
            containers_pb2.DeleteContainerRequest(id=container_id),
            metadata=self._metadata()
        )
        print(f"Container '{container_id}' deleted.")