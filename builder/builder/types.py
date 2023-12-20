from typing import TypedDict


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


class ToolList(TypedDict):
    tools: list[Tool]
