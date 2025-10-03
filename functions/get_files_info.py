import os
from os.path import join, abspath, normpath

def get_files_info(working_directory, directory="."):
    try:
        # Create the full path to the directory
        full_path = join(working_directory, directory)
        
        # Normalize the path to ensure it stays within the working directory
        full_path = normpath(full_path)
        if not full_path.startswith(normpath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        # Check if the directory exists and is a directory
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        # Build the string representation of the directory contents
        result = []
        for entry in os.listdir(full_path):
            entry_path = join(full_path, entry)
            is_dir = os.path.isdir(entry_path)
            file_size = os.path.getsize(entry_path) if not is_dir else 0
            result.append(f'- {entry}: file_size={file_size} bytes, is_dir={is_dir}')
        
        return '\n'.join(result)
    
    except Exception as e:
        return f'Error: {str(e)}'