from openai import OpenAI
import openai
import json
from json.decoder import JSONDecodeError
import sys

def read_jsx_to_string(file_path):
    with open(file_path, 'r') as file:
        jsx_content = file.read()
    return jsx_content


def read_txt(file_path):
    with open(file_path, 'r') as f:
        txt = f.read().strip()
    return txt


apikey = read_txt('./api_key.txt')
client = OpenAI(
    api_key=apikey
)

def call_gpt4(prompt):
    model_engine = "gpt-4-1106-preview"
    response = client.chat.completions.create(
        model=model_engine,
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def call_gpt_with_retries_json(user_prompt, max_retries=3):
    retry_count = 0
    while retry_count < max_retries:
        raw_response = call_gpt4(user_prompt)

        try:
            decoded_response = json.loads(raw_response)
            return decoded_response
        except JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            print(f"Problematic JSON string: {raw_response}")
            retry_count += 1

            if retry_count == max_retries:
                print("Max retries reached. Exiting.")
                sys.exit(1)


def is_valid_jsx(jsx_string):
    return True


def separate_results_page_jsx(text):
    index_jsx_start = text.find("```jsx") + len("```jsx")
    index_jsx_end = text.find("```", index_jsx_start)
    index_jsx_code = text[index_jsx_start: index_jsx_end].strip()

    return index_jsx_code


def call_gpt_with_retries_jsx(user_prompt, max_retries=3):
    retry_count = 0
    while retry_count < max_retries:
        raw_response = call_gpt4(user_prompt)
        jsx_page = separate_results_page_jsx(raw_response)
        if is_valid_jsx(jsx_page):
            return jsx_page
        else:
            retry_count += 1

            if retry_count == max_retries:
                print("Max retries reached. Exiting.")
                sys.exit(1)