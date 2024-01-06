#!/usr/bin/env python3
import os
import yaml
import argparse
from tools import Tool
from dockerfile import generate_dockerfile

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process tools from a YAML file.')
    parser.add_argument('--tools-yaml', help='Path to the tools YAML file', dest='tools', default='./tools.yaml')
    parser.add_argument('--output-dir', help='Path where the tools are installed to', dest='output', default='./dist')
    parser.add_argument('--dockerfile', help='Path where the dockerfile will be generated to', dest='dockerfile', default='./Dockerfile')
    parser.add_argument('--dockertag', help='Image tag of the container image (used for feature branches)', dest='dockertag', default='latest')

    args = parser.parse_args()

    output_dir = os.path.abspath(args.output)
    dockerfile_path = os.path.abspath(args.dockerfile)
    docker_image = f"ghcr.io/skaronator/devops-toolbox:{args.dockertag}"

    with open(args.tools, 'r') as file:
        tools_data = yaml.safe_load(file)

    tools = []
    for tool_data in tools_data['tools']:
        tool = Tool(
            output_dir=output_dir,
            docker_image=docker_image,
            **tool_data
        )
        tools.append(tool)

    all_alias = f"""#!/bin/env sh
alias toolbox-update='
    echo "Updating DevOps Toolbox"
    docker pull {docker_image}
    if [ "$(basename "$SHELL")" = "zsh" ]; then
        [ -f "$HOME/.zshrc" ] && . "$HOME/.zshrc" && echo "Reloaded .zshrc"
    else
        [ -f "$HOME/.bashrc" ] && . "$HOME/.bashrc" && echo "Reloaded .bashrc"
    fi
    echo "Update completed!"
'
"""

    for tool in tools:
        alias = tool.process()
        if alias:
            all_alias += alias + "\n"

    load_alias_file = os.path.join(args.output, "alias")
    with open(load_alias_file, "w", newline="\n") as file:
        file.write(all_alias)

    os.chmod(load_alias_file, 0o755)

    generate_dockerfile(output_dir, dockerfile_path)
