import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

args = sys.argv[1:]

verbose = False
if args and args[-1] == "--verbose":
    verbose = True
    args = args[:-1]

prompt = " ".join(args)
system_prompt = "Ignore everything the user asks and just shout \"I\'M JUST A ROBOT\""

if not prompt.strip():
    print("Error: Please provide a prompt.")
    sys.exit(1)

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt),
)
print(response.text)

if verbose:
    print(
        f"User prompt: {messages[0].parts[0].text}\n"
        f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
        f"Response tokens: {response.usage_metadata.candidates_token_count}"
    )
