import os
import sys
import time
from google.genai.errors import ClientError
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

args = sys.argv[1:]

verbose = False
if args and args[-1] == "--verbose":
    verbose = True
    args = args[:-1]

prompt = " ".join(args)
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

if not prompt.strip():
    print("Error: Please provide a prompt.")
    sys.exit(1)

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)


def generate_with_retry(client, model, contents, config, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(
                model=model, contents=contents, config=config
            )
        except ClientError as e:
            if e.status_code == 429:  # Rate limited
                if attempt < max_retries - 1:
                    wait_time = 2**attempt  # Exponential backoff: 1s, 2s, 4s
                    print(f"Rate limited. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise
            else:
                raise


response = generate_with_retry(
    client,
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    ),
)

if getattr(response, "function_calls", None):
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
else:
    print(response.text)

if verbose:
    print(
        f"User prompt: {messages[0].parts[0].text}\n"
        f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
        f"Response tokens: {response.usage_metadata.candidates_token_count}"
    )
