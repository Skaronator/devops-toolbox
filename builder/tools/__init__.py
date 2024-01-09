import os
import requests
import zipfile
import tarfile
import tempfile
import shutil
import subprocess
import time


class Tool:
    def __init__(
        self,
        name: str,
        version: str | int,
        verify_command: str,
        download_template: dict[str, str],
        output_dir: str,
        docker_image: str,
        repository: str = "",
        envs: dict[str, str] = {},
        volumes: dict[str, str] = {},
        tty: bool = True,
        interactive: bool = True,
    ):
        self.name = name
        self.version = version
        self.verify_command = verify_command
        self.docker_image = docker_image
        self.output_dir = output_dir
        self.repository = repository
        self.envs = envs
        self.volumes = volumes
        self.tty = tty
        self.interactive = interactive
        self.url = self.get_download_url(download_template)

    def process(self) -> str | None:
        self.fetch_tool()
        self.verify_tool()
        alias = self.get_alias_command()
        return alias

    def get_download_url(self, download_template) -> str | None:
        # remove v prefix from version number
        version_number = self.version.lstrip('v')
        url = download_template.format(VERSION=self.version, VERSION_NUMBER=version_number)
        return url

    def fetch_tool(self) -> None:
        os.makedirs(self.output_dir, exist_ok=True)
        output_file = os.path.join(self.output_dir, self.name)

        print(f"{'=' * 25} Installing {self.name} @ {self.version} {'=' * 25}")

        response = requests.get(self.url, stream=True)
        response.raise_for_status()

        tmp = tempfile.mkdtemp()
        file_name = os.path.basename(self.url)
        file_path = os.path.join(tmp, file_name)

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print(f"Download successful. File saved to {file_path}")

        if file_path.endswith(".zip"):
            print(f"Extacting {self.name} from {file_path} to {self.output_dir}")
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extract(self.name, self.output_dir)
        elif file_path.endswith(".tar.gz"):
            print(f"Extacting {self.name} from {file_path} to {self.output_dir}")
            with tarfile.open(file_path, 'r:gz') as tar_ref:
                for member in tar_ref.getmembers():
                    if self.name in os.path.basename(member.name):
                        with tar_ref.extractfile(member) as src, open(output_file, 'wb') as dst:
                            dst.write(src.read())
                        # exit after first match
                        break

        else:
            shutil.move(file_path, output_file)

        print(f"Adding chmod +x to {output_file}")
        os.chmod(output_file, 0o755)
        static_time = time.mktime((2077, 1, 1, 0, 0, 0, 0, 0, 0))
        os.utime(output_file, times=(static_time, static_time))

    def verify_tool(self) -> None:
        original_path = os.environ['PATH']

        print(f"{'=' * 25} Verifying command output {'=' * 25}")

        try:
            os.environ['PATH'] = f"{self.output_dir}:{original_path}"
            result = subprocess.run(self.verify_command, check=True, text=True, capture_output=True, shell=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error running the command: {e.stderr}")
            raise e
        finally:
            # Restore the original PATH
            os.environ['PATH'] = original_path

        print(f"{'=' * 25} Successfully installed {self.name}! {'=' * 25}")

    def get_alias_command(self):
        envs = " ".join(f"-e {k}={v}" for k, v in self.envs.items())
        volumes = " ".join(f"-v {s}:{d}" for s, d in self.volumes.items())

        cmd = [
            "docker",
            "run",
            "--tty" if self.tty else "",
            "--interactive" if self.interactive else "",
            "--rm",
            "--network=host",
            "--user=\"$(id -u):$(id -g)\"",
            "-e", "HOME",
            "-e", "USER",
            envs,
            "-v", "$HOME:$HOME",
            "-v", "$PWD:/workdir",
            volumes,
            self.docker_image,
            self.name,
        ]
        # remove empty strings from cmd
        cmd = [x for x in cmd if x.strip()]
        alias_command = f"alias '{self.name}'='{' '.join(cmd)}'"
        return alias_command
