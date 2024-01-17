import os


def generate_dockerfile(tools_dir, dockerfile_path):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    dockerfile = os.path.join(script_directory, "Dockerfile")
    with open(dockerfile, 'r') as existing_file:
        dockerfile_content = existing_file.read()

    files = [f for f in os.listdir(tools_dir) if os.path.isfile(os.path.join(tools_dir, f))]
    files.sort(key=lambda f: os.path.getsize(os.path.join(tools_dir, f)), reverse=True)
    top_files = files[:10]

    common_part = os.path.commonprefix([tools_dir, dockerfile_path])
    relative_tools_dir = os.path.relpath(tools_dir, common_part)

    # Generate COPY commands for the top 10 files
    copy_commands = "\n" + "\n".join([f"COPY {relative_tools_dir}/{f} /app/{f}" for f in top_files])

    # Generate a single COPY command for all other files
    other_files = set(files) - set(top_files)
    if other_files:
        copy_commands += "\n" + f"COPY {f' {relative_tools_dir}/'.join(other_files)} /app/"

    # Insert all copy_commands between 1st and 2nd line of original Dockerfile to improve caching
    dockerfile_lines = dockerfile_content.split('\n')
    first_line = dockerfile_lines[0]
    rest_of_dockerfile = '\n'.join(dockerfile_lines[1:])
    content = first_line + '\n' + copy_commands + '\n' + rest_of_dockerfile

    with open(dockerfile_path, 'w') as output_file:
        output_file.write(content)
