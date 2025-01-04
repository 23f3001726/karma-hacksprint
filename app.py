from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
