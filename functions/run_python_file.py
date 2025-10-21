import subprocess
import os
from os.path import join, normpath


def run_python_file(working_directory, file_path, args=[]):

    full_path = join(working_directory, file_path)
    full_path = normpath(full_path)
    # Check if the file is outside the working directory
    if not full_path.startswith(working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # Check if the file exists
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'

    # Check if the file is a Python file
    if not full_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        # Construct the command
        command = ["python", file_path] + args

        # Run the command
        result = subprocess.run(
            command, cwd=working_directory, capture_output=True, text=True, timeout=30
        )

        output = ""
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}"
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}"
        if not output:
            output = "No output produced."

        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
