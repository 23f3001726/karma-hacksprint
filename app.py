from flask import Flask, request, jsonify, render_template
from backend.pdfScrap import extract_text_from_pdf, summarize_text_with_llm
import requests, os
from bs4 import BeautifulSoup
from backend.isstatic import *
from backend.static import *
from backend.dynamic import *
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("pdfscrap.html")

@app.route('/summarizePdf', methods=['POST'])
def summarize_pdf():
    """Endpoint to upload a PDF, extract text, and summarize it."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    pdf_file = request.files['file']
    if not pdf_file.filename.endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400

    # Secure the uploaded file
    filename = secure_filename(pdf_file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_file.save(filepath)

    # Re-open the saved file for text extraction
    with open(filepath, 'rb') as saved_pdf_file:
        extracted_text = extract_text_from_pdf(saved_pdf_file)
        if extracted_text.startswith("Error"):
            return jsonify({"error": extracted_text}), 500

    # Summarize the extracted text using LLM
    summarized_text = summarize_text_with_llm(extracted_text)

    # Return the summary as JSON
    return jsonify({"summary": summarized_text})


@app.route('/scrape', methods=['GET'])
def get_scrape():
    return render_template('scrape.html')


@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.json.get('url')  # Extract the URL from the POST data

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        # Fetch the website content
        response = requests.get(url)
        response.raise_for_status()  # Check for successful request (200 OK)

        soup = BeautifulSoup(response.content, 'html.parser')

        flag = is_static_page(soup, len(response.content) < 10000)

        if flag :
            return scrape_static_page(soup)
        
        else :
            return scrape_dynamic_website(url)


    except requests.exceptions.RequestException as e:
        print(str(e))
        return jsonify({'error': f'Error fetching the website: {str(e)}'}), 500
    
    except Exception as e:
        print(str(e))
        return jsonify({'error': f'Error fetching the website: {str(e)}'}), 400

from backend import pdfScrap

if __name__ == '__main__':
    app.run(debug=True)
