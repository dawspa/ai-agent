
# Project Documentation

This project contains a Python-based AI agent that can perform various file operations and execute Python scripts.

## Project Structure

The project has the following directory structure:

.
├── pkg
│   ├── __pycache__
│   │   ├── calculator.cpython-310.pyc
│   │   └── render.cpython-310.pyc
│   ├── calculator.py
│   ├── morelorem.txt
│   └── render.py
├── main.py
├── README.md
├── lorem.txt
└── tests.py

## Files

- **`main.py`**: This is the main script for running the agent.
- **`README.md`**: This file contains the documentation for the project.
- **`lorem.txt`**: A sample text file.
- **`tests.py`**: Contains unit tests for the project.
- **`pkg/calculator.py`**: Contains calculator-related functions.
- **`pkg/morelorem.txt`**: Another sample text file.
- **`pkg/render.py`**: Contains functions for rendering or display.
- **`pkg/__pycache__`**: This directory contains compiled Python bytecode files.

## How to Run the Agent

1. **Navigate to the project directory**:
   ```bash
   cd /path/to/your/project
   ```

2. **Add your API to environment variables**:
   Create an `.env` in the root directory of the project.
   Add your Gemini API key there.
   ```python
   GEMINI_API_KEY="key"
   ```

2. **Run the agent using `main.py`**:
   ```bash
   python main.py #or
   uv run ./main.py "question"
   ```

## How to Ask Questions

Once the agent is running, you can interact with it by asking questions or giving commands. The agent will process your requests based on its capabilities, which include:

- Listing files and directories.
- Reading file contents.
- Executing Python files.
- Writing or overwriting files.

**Example interactions**:

- "List all files in the root directory."
- "Show me the content of `lorem.txt`."
- "Run `tests.py` with no arguments."
- "Write 'Hello, World!' to a new file named `output.txt`."
- "Fix calculation error in `calculator`."

The agent will respond with the output of the executed commands or the information you requested.