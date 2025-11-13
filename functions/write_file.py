import os
from os.path import join, normpath
from google.genai import types

MAX_CHARS = 10000


def write_file(working_directory, file_path, content):
    # Construct the absolute path of the file
    full_path = join(working_directory, file_path)
    full_path = normpath(full_path)

    # Check if the file is outside the working directory
    if not full_path.startswith(normpath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # Check if the path exists and create if neccesary
    if not os.path.exists(full_path):
        dir_path = os.path.dirname(full_path)
        if dir_path:  # Ensure directory path is not empty (for current dir files)
            os.makedirs(dir_path, exist_ok=True)

    try:
        # Write the file content
        with open(full_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file",
            ),
        },
    ),
)
