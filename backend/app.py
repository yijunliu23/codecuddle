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
    # prompt_1 = "I have a webpage that is about" + page_about + ". And have the following gaols" + goal + "Based on the function " + \
    #        functionality + \
    #        ". I want to make the webpage more inclusive by avoiding socially akward situation. To define socially akward situations, think about like individual agencies, bridging different norms, and using nudges and enables social signaling to reduce social anxiety like anonymous. " \
    #        "Output the top five important features in a JSON format like {\"features\":[{\"feature\":\"feature name\", \"description\":\"feature description\"}]}"
    # response = call_gpt_with_retries_json(prompt_1)
    response = {
  "features": [
    {
      "feature": "Anonymous Availability Submission",
      "description": "Allow users to submit their available times anonymously to ensure privacy and comfort, reducing the pressure of publicly sharing their schedules."
    },
    {
      "feature": "Diverse Calendar Support",
      "description": "Support integration with multiple calendar systems (e.g., Google Calendar, Outlook) to accommodate users from different cultural and organizational backgrounds."
    },
    {
      "feature": "Soft Reminder System",
      "description": "Implement a gentle reminder system that nudges participants to submit their availability, reducing the social burden on the organizer to chase down responses."
    },
    {
      "feature": "Flexible Timezone Handling",
      "description": "Automatically adjust for different time zones to ensure everyone can view the schedule in their local time, preventing confusion and unintentional exclusion."
    }
  ]
}
    time.sleep(10)

    return response
    

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

        improved_file_path = process_file(filepath)

        return send_file(improved_file_path, as_attachment=True)

def process_file(filepath):
    filepath = "uploads/App.js"
    return filepath


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