from flask import Flask, send_from_directory, request, jsonify, send_file
from werkzeug.utils import secure_filename
from json.decoder import JSONDecodeError
from openai import OpenAI
import os
import json
import sys
import time



app = Flask(__name__, static_folder='../build/static', template_folder='../build')

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    return send_from_directory(app.template_folder, 'index.html')


@app.route('/submit-form', methods=['POST'])
def handle_form():
    data = request.json
    page_about = data.get('pageAbout', 'No data')
    goal = data.get('goal', 'No data')
    functionality = data.get('functionality', 'No data')
    features_response = get_features(functionality, goal, page_about)
    return jsonify(features_response)


def get_features(functionality, goal, page_about):
    prompt_1 = "I have a webpage that is about" + page_about + ". And have the following gaols" + goal + "Based on the function " + \
           functionality + \
           ". Now, I want to make the webpage more inclusive by avoiding socially awkward situations, reducing the anxiety for users to use the website, and bringing all users together regardless of their backgrounds such as language, ethnicity, and educational levels by making them feel comfortable while using the website. "\
            "Some examples include using nudges and social signalings, or display pre-written notices to make sure of the language use. Please make sure that the function is not a broad term but can be implemented through one-step change in JavaScript. Remeber to be very specific in terms of the functionality, do not include features relating to UI, cultural calender, accessibility, real-time, or user profiles." \
           "Do not mention UI. No visual features. No real-time systems. Output the top seven important features in a JSON format like {\"features\":[{\"feature\":\"feature name\", \"description\":\"feature description\"}]}"
    response = call_gpt_with_retries_json(prompt_1)

    print(response)

    prompt_2 = f"""
        Below is a list of features that intend to improve social inclusiveness in websites, defined as the prevention of social anxiety, awkwardness, and isolation, while fostering synchronization among users from diverse backgrounds in their use of online collaborative technologies.
        {response}.
        For each feature, please firstly rate them based on these two evaluation metrics:
        Social Inclusiveness: This metric evaluates whether the generated features are directly related to social inclusiveness rather than other forms of inclusiveness, such as accessibility or UI design. Features that specifically address social inclusion are considered successful.
        Feasibility: This metric assesses the complexity and practicality of implementing the generated features. Features that are straightforward to implement and do not require complex systems such as a changes in the javascript that do not require external packages are considered feasible. Features that are overly complicated or impractical to implement such as AI or real-time modifications are regarded as infeasible.
        Please rate each feature on a scale of 1 to 5, where 1 indicates the lowest rating and 5 indicates the highest rating. For each feature, provide two ratings.:
        Now, please only return the top 5 features based on the ratings' sum for each feature, return in this json format:

        {{"features":[
            {{"feature":"feature name", "description":"feature description", "social_inclusiveness":"1", "feasibility":"1"}}]
        }}
    """


    response_2 = call_gpt_with_retries_json(prompt_2)
    print(response_2)

    return response_2
    

# @app.route('/improve-feature', methods=['POST'])
# def improve_feature():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     if file:
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)

#         improved_file_path = process_file(filepath)

#         return send_file(improved_file_path, as_attachment=True)

# def process_file(filepath):
#     time.sleep(2000)
#     return None


@app.route('/improve-feature', methods=['POST'])
def improve_feature():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read the contents of the file
        with open(filepath, 'r') as f:
            original_code = f.read()
        # Get the feature from the request
        feature = request.form.get('feature')
        # Combine the original code with the feature using the LLM algorithm
        modified_code = combine_code(original_code, feature)
        # Save the modified code to a new file
        improved_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'improved_' + filename)
        with open(improved_file_path, 'w') as f:
            f.write(modified_code)
        
        return send_file(improved_file_path, as_attachment=True)

def combine_code(original_code, feature):
    json_code_instructions = generate_json_code_instructions(original_code, feature)
    attempt = 1
    max_attempts = 3
    original_lines = original_code.split('\n')
    line_offset = 0
    for instruction in json_code_instructions.get("instructions", []):
        if "change_type" not in instruction or "lines" not in instruction or "code" not in instruction:
            print(f"Invalid instruction format: {instruction}")
            continue
        if instruction["change_type"] == "replace":
            if contains_phrases(instruction["code"]):
                while attempt <= max_attempts:
                    instruction = prompt_again_to_fill_replace_lines()
                    attempt += 1
            attempt = 1
            original_lines, line_offset = replace_lines(original_lines, instruction, line_offset)
        elif instruction["change_type"] == "add":
            original_lines, line_offset = add_lines(original_lines, instruction, line_offset)
    new_code = '\n'.join(original_lines)
    functional_code = make_functional(new_code)
    print(functional_code)
    return functional_code["Code"]

def make_functional(code):
    prompt = f"""
    Please make this code below functional and able to compile. 

    {code}.

    Return in the following JSON format:
    {{"Code":"<Python code here>"}}
    """

    return call_gpt_with_retries_json(prompt)


def contains_phrases(code):
    phrases = ["fill", "your code", "rest of", "existing code", "original"]
    for phrase in phrases:
        if phrase in code:
            return True
    return False

def is_shorter(new_lines, original_lines):
    return len(new_lines) < len(original_lines)

# progress bar in showing the changes 

def generate_json_code_instructions(original_code, feature):
    prompt = f"""
    You are tasked with modifying an existing Python file. When modifying the code, please output the changes in the following JSON format, accommodating two change types (add and replace):

    {{"instructions":[
        {{"change_type": "add", "lines": "(12)", "code":"<Python code here>"}},
        {{"change_type": "replace", "lines": "(1,10)", "code":"<Python code here>"}}]
    }}

    When adding a new code snippet, please specify only the lines where the code should be inserted; when replacing existing code, please indicate the starting and ending lines of the code to be replaced in the format (1,10).

    The feature I would like you to implement is: {feature}.

    And here's the existing Python code: {original_code}.

    Please add only the necessary code snippets required to realize the desired functionality, keeping the code concise. Be cautious when replacing any lines, and ensure that you do not comment out any code that is still needed.

    Additionally, please be mindful to import packages in the first line; please make sure all the variables used are defined prior to using them. Count the first line as line 1. DO NOT WRITE WITHIN A FUNCTION.
    """
    
    # Use LLM to generate JSON code instructions based on the prompt
    json_code_instructions = call_gpt_with_retries_json(prompt)
    print(json_code_instructions)
    
    return json_code_instructions

def prompt_again_to_fill_replace_lines():
    prompt = f"""
    I have noticed that there are commented lines in the code snippet indicating the inclusion of the original code. Here is the new code snippet: [code returned from the last prompt with numbered lines]. And here is my original code: [user code]. Could you please replace the commented lines with the necessary code that needs to be added?

    Please return the modified code in the following JSON format:
    {{"CodeChanges":[
        {{"change_type": "replace", "lines": "(1,10)", "code":"<new, uncommented Python code>"}}]
    }}
    """
    
    # Use LLM to generate updated JSON code instructions based on the prompt
    updated_instruction = call_gpt_with_retries_json(prompt)
    
    return updated_instruction

def replace_lines(original_lines, instruction, line_offset):
    lines_to_replace = instruction["lines"]
    if ',' in lines_to_replace:
        start_line, end_line = map(int, lines_to_replace[1:-1].split(','))
    else:
        start_line = end_line = int(lines_to_replace[1:-1])
    start_line += line_offset
    end_line += line_offset
    new_code = instruction["code"]
    modified_lines = original_lines[:start_line - 1] + [new_code] + original_lines[end_line:]
    line_offset += len(new_code.split('\n')) - (end_line - start_line + 1)
    return modified_lines, line_offset

def add_lines(original_lines, instruction, line_offset):
    lines_to_add = instruction["lines"]
    if ',' in lines_to_add:
        start_line, end_line = map(int, lines_to_add[1:-1].split(','))
        start_line += line_offset
        end_line += line_offset
        new_code_lines = instruction["code"].split('\\n')
        modified_lines = original_lines[:start_line] + new_code_lines + original_lines[start_line:]
        line_offset += len(new_code_lines)
    else:
        line_to_add = int(lines_to_add[1:-1])
        line_to_add += line_offset
        new_code = instruction["code"]
        modified_lines = original_lines[:line_to_add] + [new_code] + original_lines[line_to_add:]
        line_offset += 1
    return modified_lines, line_offset

def read_jsx_to_string(file_path):
    with open(file_path, 'r') as file:
        jsx_content = file.read()
    return jsx_content


def read_txt(file_path):
    with open(file_path, 'r') as f:
        txt = f.read().strip()
    return txt


apikey = "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"
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