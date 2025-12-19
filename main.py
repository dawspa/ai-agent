import argparse
import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import system_prompt
from call_function import call_function, available_functions


def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    generate_content(client, messages, args.verbose)


def generate_content(client, messages, verbose):
    max_iterations = 20

    for iteration in range(max_iterations):
        try:
            #time.sleep(1)
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
            # Check and print token usage
            if response.usage_metadata:
                if verbose:
                    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            else:
                raise RuntimeError("API response missing usage metadata")

            for candidate in response.candidates:
                messages.append(candidate.content)

            # Handle response without function calls
            if response.function_calls:
                # Collect function responses
                function_responses = []
                for function_call_part in response.function_calls:
                    function_call_result = call_function(function_call_part, verbose)
                    # 1. Check if the parts list is empty
                    if not function_call_result.parts:
                        raise Exception("empty function call result")

                    # 2. Extract the actual Part object from the list
                    result_part = function_call_result.parts[0]

                    # 3. Check for function_response on the Part object
                    if not result_part.function_response:
                        raise Exception("empty function call result content")

                    if verbose:
                        # Print the actual response payload
                        print(f"-> {result_part.function_response.response}")

                    # 4. Append the PART object, not the list of parts
                    function_responses.append(result_part)

                # Add function responses as a user message
                messages.append(
                    types.Content(role="user", parts=function_responses)
                )
                # Continue the loop to let the model process the results
                continue

            # Check if we're done (no function calls and has text)
            if response.text:
                print(f"Final response:\n{response.text}")
                break

        except Exception as e:
            print(f"Error during iteration {iteration + 1}: {e}")
            break

    return response.text if response.text else None

if __name__ == "__main__":
    main()
