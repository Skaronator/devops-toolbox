#!/usr/bin/env python3
import os
import yaml
import argparse
import platform
from builder.types import Tool, ToolList
from builder.fetch import fetch_tool
from builder.verify import verify_tool


def process_tool(tool: Tool, output_dir) -> None:
    arch = platform.machine()
    name = tool['name']

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


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process tools from a YAML file.')
    parser.add_argument('--tools-yaml', help='Path to the tools YAML file', dest='tools', default='../tools.yaml')
    parser.add_argument('--output-dir', help='Path where the tools are installed to', dest='output', default='../dist')

    args = parser.parse_args()

    with open(args.tools, 'r') as file:
        tools: ToolList = yaml.safe_load(file)

    for tool in tools['tools']:
        process_tool(tool, args.output)

    output_file = os.path.join(args.output, 'versions.txt')
    with open(output_file, 'w') as output_file:
        sorted_tools = sorted(tools['tools'], key=lambda x: x['name'])
        for tool in sorted_tools:
            name = tool['name']
            version = tool['version']
            output_file.write(f"{name}: {version}\n")
