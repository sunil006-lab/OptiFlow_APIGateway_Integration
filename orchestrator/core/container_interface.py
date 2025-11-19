import subprocess

class ContainerdInterface:
    def list_containers(self):
        return self._run_cmd(['ctr', 'containers', 'list'])

    def list_images(self):
        return self._run_cmd(['ctr', 'images', 'list'])

    def pull_image(self, image: str):
        return self._run_cmd(['ctr', 'images', 'pull', image])

    def run_container(self, image: str, container_name: str):
        return self._run_cmd(['ctr', 'run', '--rm', '-t', image, container_name])

    def delete_container(self, container_name: str):
        return self._run_cmd(['ctr', 'containers', 'delete', container_name])

    def _run_cmd(self, cmd_list):
        try:
            result = subprocess.run(cmd_list, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"[ERROR] {e.stderr.strip()}"
