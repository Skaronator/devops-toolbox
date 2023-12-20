#!/usr/bin/env python3
import os
import yaml
import argparse
import platform
from builder.types import Tool, ToolList
from builder.fetch import fetch_tool
from builder.verify import verify_tool

DOCKER_IMAGE = "ghcr.io/skaronator/devops-toolbox:latest"


def process_tool(tool: Tool, output_dir) -> str:
    arch = platform.machine()
    name = tool['name']
    docker_command = tool.get('docker_command', "")

    version = tool['version']
    # remove v prefix from version number
    version_number = version.lstrip('v')

    verify_command = tool['verify_command']
    download_template = tool['download_template'][arch]
    download_url = download_template.format(VERSION=version, VERSION_NUMBER=version_number)

    print(f"{'=' * 25} Installing {name} @ {version} {'=' * 25}")

    fetch_tool(output_dir, download_url, name)
    verify_tool(output_dir, verify_command)

    print(f"{'=' * 25} Successfully installed {name}! {'=' * 25}")

    alias_command = f"alias '{name}'='docker run -it --rm -e HOME -e USER -v $PWD:/workdir {docker_command} {DOCKER_IMAGE} {name}'"
    return alias_command


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process tools from a YAML file.')
    parser.add_argument('--tools-yaml', help='Path to the tools YAML file', dest='tools', default='../tools.yaml')
    parser.add_argument('--output-dir', help='Path where the tools are installed to', dest='output', default='../dist')

    args = parser.parse_args()

    with open(args.tools, 'r') as file:
        tools: ToolList = yaml.safe_load(file)

    all_alias = "#!/bin/sh" + "\n"
    all_alias += f"alias 'toolbox-update'='docker pull {DOCKER_IMAGE}'" + "\n"
    for tool in tools['tools']:
        alias = process_tool(tool, args.output)
        all_alias += alias + "\n"

    load_alias_file = os.path.join(args.output, "alias")
    with open(load_alias_file, "w", newline="\n") as file:
        file.write(all_alias)

    os.chmod(load_alias_file, 0o755)
