import os
from os.path import join, normpath
from google.genai import types

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    # Construct the absolute path of the file
    full_path = join(working_directory, file_path)
    full_path = normpath(full_path)

    # Check if the file is outside the working directory
    if not full_path.startswith(normpath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # Check if the path is a regular file
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        # Read the file content
        with open(full_path, "r") as f:
            file_content = f.read()

        # Truncate if needed
        if len(file_content) > MAX_CHARS:
            file_content = (
                file_content[:MAX_CHARS]
                + f' [...File "{file_path}" truncated at 10000 characters]'
            )

        return file_content
    except Exception as e:
        return f"Error: {str(e)}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read content of a regular file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to read, relative to the working directory.",
            ),
        },
    ),
)
