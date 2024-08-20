from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    try:
        # Send a GET request to fetch the raw HTML content
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all div elements with the class 'blockSeries'
        block_series_divs = soup.find_all('div', class_='blockSeries')
        
        # Initialize a counter for episodes
        episode_number = 1
        src_links = []

        # Extract src attributes from iframes within these divs
        for div in block_series_divs:
            link = div.find('a')
            if link:
                epUrl = link.get('href') + "watch/"
                response = requests.get(epUrl)
                soup = BeautifulSoup(response.text, 'html.parser')
                iframes = soup.find_all('iframe')
                for iframe in iframes:
                    src = iframe.get('src')
                    if src:
                        src_links.append(src)
                        episode_number += 1

        return jsonify({'srcLinks': src_links})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
