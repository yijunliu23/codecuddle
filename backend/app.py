from flask import Flask, send_from_directory, request, jsonify, send_file
from aux import call_gpt_with_retries_json
import os
from werkzeug.utils import secure_filename


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

# call for each one agency rules etc. 

def get_features(functionality, goal, page_about):
    prompt_1 = "I have a webpage that is about" + page_about + ". And have the following gaols" + goal + "Based on the function " + \
           functionality + \
           ". I want to make the webpage more inclusive by avoiding socially akward situation. " \
           "Output the top five important features in a JSON format like \"features\":[{\"feature\":\"feature name\", \"description\":\"feature description\", " \
                                    "\"location\": \"location on the main page, like left, right, center\"}]}"
    response = call_gpt_with_retries_json(prompt_1)
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
    return filepath
