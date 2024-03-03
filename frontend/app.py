from flask import Flask, render_template, request
import requests
from etherscan import Client
from bs4 import BeautifulSoup
import re
from PIL import Image
from PIL.ExifTags import TAGS
import exifread

app = Flask(__name__)

# Initialize Etherscan client
es = Client(api_key='TMFZA9NKDREWR4MJUA2AJR8V1U4AVRV6RX')

dangerous_keywords = ['preteen', 'loli', 'lolita', 'jailbait', 'pthc', 'best cp',
                      'child porn', 'kid porn', 'child sex', 'cp video',
                      'nude children', 'cp porn', 'free child porn', 'kinderporn',
                      'child rape', 'toddler porn', 'kids videos', 'cp videos',
                      'lolilust', 'pedo porno', 'pedo content', 'underage', 'cp pack',
                      'loliporn', 'pedofamily', 'cp database', 'pedo webcams', 'lolitacity',
                      'xxx child', 'xxx underage', 'young forbidden']

# Function to make TOR request
def make_tor_request(url):
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    try:
        response = requests.get(url, proxies=proxies)
        return response
    except Exception as e:
        print("Error:", e)
        return None

# Function to display directory URLs
def display_directory_urls(response):
    directory_urls = []
    if not response:
        print("No response received.")
        return directory_urls

    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a')
    if links:
        for link in links:
            href = link.get('href')
            if href and (href.startswith("http://") or href.startswith("https://")):
                directory_urls.append(href)
    return directory_urls

# Route for index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for main page
@app.route('/main', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        return render_template('main.html')
    else:
        return "Method Not Allowed", 405

# Route for parsing directory
@app.route('/parse_directory', methods=['GET', 'POST'])
def parse_directory():
    if request.method == 'POST':
        onion_url = request.form['onion_url']
        response = make_tor_request(onion_url)
        if response and response.status_code == 200:
            directory_urls = display_directory_urls(response)
            if directory_urls:
                return render_template('parse_directory.html', directory_urls=directory_urls)
            else:
                return render_template('parse_directory.html', directory_urls=[], error_message="No directory URLs found.")
        else:
            return render_template('parse_directory.html', directory_urls=[], error_message="Failed to retrieve directory listing or status code is not 200.")
    else:
        return render_template('parse_directory.html')

# Route for analyzing cryptocurrency transactions
@app.route('/analyse_transaction', methods=['GET','POST'])
def analyse_transaction():
    if request.method == 'POST':
        crypto_address = request.form['crypto_address']
        # Fetch actual transaction information based on the crypto address
        eth_balance = es.get_eth_balance(crypto_address)
        eth_transactions = es.get_transactions_by_address(crypto_address)
        
        return render_template('analyse_transaction.html', eth_balance=eth_balance, eth_transactions=eth_transactions)
    elif request.method == 'GET':
        return render_template('analyse_transaction.html', eth_balance=None, eth_transactions=None)
    else:
        return "Method Not Allowed", 405

# Function to fetch transaction value for a cryptocurrency address
def get_value(crypto_address):
    # Make a request to the blockchain API to get the transaction details for the given address
    endpoint = f"https://api.blockchain.com/v1/address/{crypto_address}/transactions"
    response = requests.get(endpoint)
    if response.status_code == 200:
        try:
            data = response.json()
            if data:
                return data[0].get("value")
        except Exception as e:
            print("Error decoding JSON response:", e)
            return None
    else:
        print("Failed to fetch value. Status code:", response.status_code)
        return None

# Route for keyword search
@app.route('/search', methods=['GET', 'POST'])
def keyword():
    if request.method == 'POST':
        # Handle POST request
        user_input = request.form['keyword']
        bold_word = f'<strong>{user_input}</strong>'

        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

        input_file_path = 'output.txt'  # Change this to your input file path
        with open(input_file_path, 'r') as file:
            lines = file.readlines()

        matching_lines = [line.strip().replace(user_input, bold_word) for line in lines if user_input.lower() in line.lower()]

        return render_template('keyword.html', matching_lines=matching_lines, user_input=user_input)
    else:
        # Handle GET request
        return render_template('keyword.html')





def get_exif_data(image):
    exif_data = image._getexif()
    if exif_data is not None:
        exif = {}
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            exif[tag_name] = value
        return exif
    return None

def convert_to_degrees(value):
    d, m, s = value
    return d + m / 60.0 + s / 3600.0

def get_gps_coordinates(image):
    with open(image.filename, 'rb') as f:
        exif_tags = exifread.process_file(f)
        gps_latitude = exif_tags.get('GPS GPSLatitude')
        gps_longitude = exif_tags.get('GPS GPSLongitude')
        gps_latitude_ref = exif_tags.get('GPS GPSLatitudeRef')
        gps_longitude_ref = exif_tags.get('GPS GPSLongitudeRef')
        if gps_latitude and gps_longitude and gps_latitude_ref and gps_longitude_ref:
            latitude = convert_to_degrees(gps_latitude.values)
            longitude = convert_to_degrees(gps_longitude.values)
            return {
                'latitude': latitude,
                'longitude': longitude,
                'latitude_ref': gps_latitude_ref.values,
                'longitude_ref': gps_longitude_ref.values,
                'location': get_location_from_coordinates(latitude, longitude)
            }
    return None

def get_location_from_coordinates(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}&zoom=18&addressdetails=1"
    
    try:
        response = requests.get(url)
        data = response.json()
        address = data.get('display_name', 'Location not found')
        return address
    except Exception as e:
        print("Exception:", str(e))
        return None


@app.route('/process_image', methods=['GET','POST'])
def process_image():
    if request.method == 'POST':
        if 'image' in request.files:
            image = request.files['image']
            # Check if the image file is empty
            if image.filename == '':
                error_message = "No image uploaded."
                return render_template('exif.html', error_message=error_message)
            try:
                # Open the image and extract EXIF data
                img = Image.open(image)
                exif_data = get_exif_data(img)
                return render_template('exif.html', exif_data=exif_data)
            except Exception as e:
                error_message = "Error processing image: " + str(e)
                return render_template('exif.html', error_message=error_message)
        else:
            error_message = "No image uploaded."
            return render_template('exif.html', error_message=error_message)
    else:
        return render_template('exif.html')

def get_exif_data(image):
    exif_data = image._getexif()
    if exif_data is not None:
        exif = {}
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            exif[tag_name] = value
        return exif
    return None


@app.route('/userinfo', methods=['GET'])
def userinfo():
    query = request.args.get('query')
    if not query:
        return render_template('userinfo.html', error="No query provided.")

    url = "https://api.proxynova.com/comb"
    params = {"query": query}

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        lines = data.get("lines", [])
        return render_template('userinfo.html', results=lines)
    else:
        return render_template('userinfo.html', error=f"Error: {response.status_code}")


if __name__ == '__main__':
    app.run(debug=True)

