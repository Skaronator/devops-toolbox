from typing import TypedDict


class Tool(TypedDict):
    name: str
    version: str | int
    verify_command: str
    download_template: dict[str, str]


class ToolList(TypedDict):
    tools: list[Tool]
