from typing import TypedDict


class Tool(TypedDict):
    name: str
    version: str | int
    verify_command: str
    docker_command: str | None
    download_template: dict[str, str]


class ToolList(TypedDict):
    tools: list[Tool]
