from flask import Flask, request, jsonify, render_template
from backend.pdfScrap import extract_text_from_pdf, summarize_text_with_llm
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    return render_template("index.html")

@app.route('/summarizePdf', methods=['POST'])
def summarize_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    pdf_file = request.files['file']
    if not pdf_file.filename.endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400

    # Extract text from PDF
    extracted_text = extract_text_from_pdf(pdf_file)
    if extracted_text.startswith("Error"):
        return jsonify({"error": extracted_text}), 500

    # Summarize text using Gemini LLM API
    summarized_text = summarize_text_with_llm(extracted_text)
    if summarized_text.startswith("Error"):
        return jsonify({"error": summarized_text}), 500

    return jsonify({"summary": summarized_text})

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

        # Scrape specific data (title, meta description, and links)
        title = soup.title.string if soup.title else "No Title Found"
        description = soup.find('meta', attrs={'name': 'description'})
        description = description['content'] if description else "No Description Found"
        
        # Extract all links from the page
        links = [a['href'] for a in soup.find_all('a', href=True)]

        # Return the scraped data as JSON
        return jsonify({
            'title': title,
            'description': description,
            'links': links
        })

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error fetching the website: {str(e)}'}), 500
    
from backend import pdfScrap

if __name__ == '__main__':
    app.run(debug=True)
