from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import random

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
@app.route('/random', methods=['GET'])
def get_random_number():
    random_number = random.randint(1, 14)
    return jsonify({'random_number': random_number})
@app.route('/home', methods=['GET'])
def get_scraped_data():
    url = 'https://joycinema.store/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d9%83%d8%b1%d8%aa%d9%88%d9%86-%d9%85%d8%aa%d8%b1%d8%ac%d9%85%d8%a9/'  # Replace with the specific URL you want to scrape
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Failed to retrieve data from the website"}), 500

    soup = BeautifulSoup(response.content, 'html.parser')

    post_blocks = soup.find_all('div', class_='postBlockOne')

    data = []
    for post in post_blocks:
        title = post.find('h3', class_='title').text
        link = post.find('a', class_='series')['href']
        imgdiv = post.find('div', class_='poster')
        img = imgdiv.find('img')['data-img']

        data.append({
            'title': title,
            'link': link,
            'image': img
        })

    return jsonify(data)
    
@app.route('/')
def index():
    return 'gg'
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
    import os
    port = int(os.environ.get('PORT', 4000))
    app.run(host='0.0.0.0', port=port)
