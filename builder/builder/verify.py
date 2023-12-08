import subprocess
import os


def verify_tool(output_dir, command):
    original_path = os.environ['PATH']

    print(f"{'=' * 25} Verifying command output {'=' * 25}")

    try:
        os.environ['PATH'] = f"{output_dir}:{original_path}"
        result = subprocess.run(command, check=True, text=True, capture_output=True, shell=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running the command: {e.stderr}")

    finally:
        # Restore the original PATH
        os.environ['PATH'] = original_path
