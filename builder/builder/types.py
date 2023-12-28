from typing import TypedDict
import platform

ARCH = platform.machine()


class Tool:
    def __init__(
        self,
        name: str,
        version: str | int,
        verify_command: str,
        download_template: dict[str, str],
        repository: str = "",
        docker_command: str = "",
        tty: bool = True,
        interactive: bool = True,
    ):
        self.name = name
        self.version = version
        self.verify_command = verify_command
        self.docker_command = docker_command
        self.repository = repository
        self.tty = tty
        self.interactive = interactive
        self.download_template = download_template

    def get_download_url(self) -> str | None:
        # remove v prefix from version number
        version_number = self.version.lstrip('v')
        download_template = self.download_template.get(ARCH)
        if download_template is None:
            return None
        url = download_template.format(VERSION=self.version, VERSION_NUMBER=version_number)
        return url


class ToolList(TypedDict):
    tools: list[Tool]
