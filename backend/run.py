from flask import Flask, jsonify, request
from flask_cors import CORS
from app import llm
import os
import re
import aspose.words as aw
from werkzeug.utils import secure_filename

from docx import Document

app = Flask(__name__)

# Example route

CORS(app)


@app.route('/')
def home():
    return "Backend!"


@app.route('/html')
def get_html():
    with open('temp/output.html') as file:
        return file.read(), 200, {'Content-Type': 'text/html'}


# Supported file extensions for processing
ALLOWED_EXTENSIONS = {'docx', 'pdf', 'txt', 'html'}

# Helper function to check file extension


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def pdf_to_html(temp_file):
    doc = aw.Document(temp_file)
    doc.save("output2.html")

    with open("output2.html", "r", encoding="utf-8") as file:
        html_string = file.read()
    html_string = re.sub(
        r'<meta name="generator" content="Aspose.Words for Python via .NET [^"]*" ?/?>', '', html_string)

    # Remove Aspose evaluation messages and links
    html_string = re.sub(
        r'<p[^>]*><span[^>]*>Created with an evaluation copy of Aspose\.Words\..*?</a></p>',
        '',
        html_string,
        flags=re.DOTALL
    )

    # Remove footer messages mentioning Aspose
    html_string = re.sub(
        r'<div[^>]*-aw-headerfooter-type:footer-primary[^>]*>.*?Created with Aspose\.Words[^<]*</span></p></div>',
        '',
        html_string,
        flags=re.DOTALL
    )

    # Clean up extra spaces or empty tags that may result from removal
    html_string = re.sub(r'\s*\n\s*', '\n', html_string)
    # Remove empty <p> tags
    html_string = re.sub(r'<p[^>]*>\s*</p>', '', html_string)
    html_string = re.sub(r'<div[^>]*>\s*</div>', '', html_string)
    os.remove("output2.001.png")
    os.remove("output2.html")
    # Remove empty <div> tags

    # Output the cleaned HTML string
    return (html_string)  # For PDF to text conversion


def docx_to_html(temp_path):
    doc = aw.Document(temp_path)
    doc.save("Output.html")

    with open("output.html", "r", encoding="utf-8") as file:
        html_string = file.read()
    html_string = re.sub(
        r'<meta name="generator" content="Aspose.Words for Python via .NET [^"]*" ?/?>', '', html_string)

    # Remove Aspose evaluation messages and links
    html_string = re.sub(
        r'<p[^>]*><span[^>]*>Created with an evaluation copy of Aspose\.Words\..*?</a></p>',
        '',
        html_string,
        flags=re.DOTALL
    )

    # Remove footer messages mentioning Aspose
    html_string = re.sub(
        r'<div[^>]*-aw-headerfooter-type:footer-primary[^>]*>.*?Created with Aspose\.Words[^<]*</span></p></div>',
        '',
        html_string,
        flags=re.DOTALL
    )

    # Clean up extra spaces or empty tags that may result from removal
    html_string = re.sub(r'\s*\n\s*', '\n', html_string)
    # Remove empty <p> tags
    html_string = re.sub(r'<p[^>]*>\s*</p>', '', html_string)
    # Remove empty <div> tags
    html_string = re.sub(r'<div[^>]*>\s*</div>', '', html_string)

    html_string = re.sub(
        r'<div\s+style="-aw-headerfooter-type:header-primary; clear:both">.*?</div>', '', html_string)

    # Output the cleaned HTML string
    os.remove("output.001.png")
    os.remove("Output.html")

    return (html_string)


@app.route('/api/data', methods=['POST'])
def get_data():
    # Get text and standard from JSON

    origin = 'html'

    input_text = request.form.get('text', '')
    standard = request.form.get('standard', '')

    # Check if input_text is empty and try to get it from the uploaded file
    if 'file1' in request.files:
        file = request.files['file1']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            temp_path = os.path.join('temp', filename)  # Save file temporarily

            file.save(temp_path)  # Save uploaded file
            ext = filename.rsplit('.', 1)[1].lower()

            # Extract text based on file extension
            if ext == 'docx':
                origin = 'docx'
                input_text = docx_to_html(temp_path)
            elif ext == 'pdf':
                origin = 'pdf'
                input_text = pdf_to_html(temp_path)
            elif ext == 'txt' or ext == 'html':
                with open(temp_path, 'r', encoding='utf-8') as f:
                    input_text = f.read()

            os.remove(temp_path)  # Clean up temporary file

    # Check if standard is empty and try to get it from the uploaded file
    if 'file2' in request.files:
        file = request.files['file2']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            temp_path = os.path.join('temp', filename)

            file.save(temp_path)
            ext = filename.rsplit('.', 1)[1].lower()

            # Extract standard based on file extension
            if ext == 'docx':
                standard = docx_to_html(temp_path)
            elif ext == 'pdf':
                standard = pdf_to_html(temp_path)
            elif ext == 'txt' or ext == 'html':
                with open(temp_path, 'r', encoding='utf-8') as f:
                    standard = f.read()

            os.remove(temp_path)

    file_path = "temp/output.html"
    # Writing the content to the file
    with open(file_path, "w") as file:  # "w" mode overwrites the file; use "a" to append
        file.write(input_text)

    sections = llm.parse_check(input_text, standard, [], origin)

    structured_data = {}
    for i in range(0, len(sections), 2):
        if i + 1 < len(sections):  # Ensure there's a corresponding content
            structured_data[sections[i]] = sections[i + 1]

    file_path = "temp/str.txt"
    with open(file_path, "w") as file:  # "w" mode overwrites the file; use "a" to append
        str = ''
        for i in range(1, len(sections), 2):
            str += sections[i]
        file.write(str)

    return jsonify(structured_data)


@app.route('/api/new', methods=['POST'])
def get_suggestion():
    suggestion = request.form.get('suggestion', '')

    file_path = "temp/output.html"
    with open(file_path, "r") as file:  # "w" mode overwrites the file; use "a" to append
        html = file.read()

    file_path = "temp/str.txt"
    with open(file_path, "r") as file:  # "w" mode overwrites the file; use "a" to append
        answer = file.read()

    text = llm.human_correction(suggestion, answer, html, [])
    text, html = llm.get_html_from_str(text)

    file_path = "temp/output.html"
    with open(file_path, "w") as file:  # "w" mode overwrites the file; use "a" to append
        file.write(html)

    print(text)

    return jsonify({'message': text})


if __name__ == '__main__':
    app.run(debug=True)
