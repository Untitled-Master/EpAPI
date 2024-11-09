from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import random
import string
import firebase_admin
from firebase_admin import credentials, db


app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Initialize Firebase Admin SDK
cred = credentials.Certificate("crss-58a32-firebase-adminsdk-xme9f-307b31b892.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://crss-58a32-default-rtdb.firebaseio.com'  # Replace with your Firebase DB URL
})

@app.route('/home2', methods=['GET'])
def get_scraped_data02():
    url = 'https://joyman.store/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a/'  # Replace with the specific URL you want to scrape
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
    
@app.route('/mv', methods=['GET'])
def get_scraped_datamv():
    url = 'https://joycinema.store/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%a7%d8%ac%d9%86%d8%a8%d9%8a/'  # Replace with the specific URL you want to scrape
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
# Define the route for the API
@app.route('/search', methods=['GET'])
def search_movies():
    query = request.args.get('query', 'House')  # Get the search query from URL parameter, default to 'House'
    url = f'https://joycinema.store/?s={query}'
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({'error': 'Could not fetch the page'}), 500

    soup = BeautifulSoup(response.content, 'html.parser')
    post_blocks = soup.find_all('div', class_='postBlockOne')

    data = []
    for post in post_blocks:
        title = post.find('h3', class_='title')
        if title:
            title = title.text
        else:
            continue  # Skip this post if there's no title

        # Extract the anchor tag and then get the href attribute for the link
        link_tag = post.find('a', class_='series')
        if link_tag:
            link = link_tag.get('href')
        else:
            link = 'No link available'  # Handle missing link case

        # Extract the image URL
        imgdiv = post.find('div', class_='poster')
        if imgdiv:
            img = imgdiv.find('img')['data-img']
        else:
            img = 'No image available'  # Handle missing image case

        data.append({
            'title': title,
            'link': link,
            'image': img
        })

    return jsonify(data)
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 4000))
    app.run(host='0.0.0.0', port=port)
