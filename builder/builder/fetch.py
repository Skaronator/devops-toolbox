import os
import requests
import zipfile
import tarfile
import tempfile
import shutil


def fetch_tool(output_dir, url, name):
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, name)

    response = requests.get(url, stream=True)
    response.raise_for_status()

    tmp = tempfile.mkdtemp()
    file_name = os.path.basename(url)
    file_path = os.path.join(tmp, file_name)

    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)
    print(f"Download successful. File saved to {file_path}")

    if file_path.endswith(".zip"):
        print(f"Extacting {name} from {file_path} to {output_dir}")
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extract(name, output_dir)
    elif file_path.endswith(".tar.gz"):
        print(f"Extacting {name} from {file_path} to {output_dir}")
        with tarfile.open(file_path, 'r:gz') as tar_ref:
            for member in tar_ref.getmembers():
                if name in os.path.basename(member.name):
                    with tar_ref.extractfile(member) as src, open(output_file, 'wb') as dst:
                        dst.write(src.read())

    else:
        shutil.move(file_path, output_file)

    print(f"Adding chmod +x to {output_file}")
    os.chmod(output_file, 0o755)
