from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup  # Import BeautifulSoup for HTML parsing

app = Flask(__name__)

# Function to extract image URLs from HTML content
def extract_images_from_html(html_content, base_url):
  """ Extracts image source URLs from the provided HTML content, 
      considering the base URL for relative links. """
  soup = BeautifulSoup(html_content, 'html.parser')
  images = []
  for img in soup.find_all('img'):
    # Extract image source URL (handle cases with and without 'src' attribute)
    image_url = img.get('src')
    if image_url:
      # If the URL is relative, prepend the base URL
      if not image_url.startswith(('http://', 'https://')):
        image_url = f"{base_url}/{image_url}"
      images.append(image_url)
  return images

# Route for rendering the HTML form
@app.route('/', methods=['GET'])
def index():
  """ Renders a basic HTML form """
  return render_template('index.html')
# Route for handling image extraction request
@app.route('/extract', methods=['POST'])
def extract_images():
  """ Extracts images from the provided URL and returns them as JSON """
  url = request.form.get('url')
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise exception for non-200 status codes
    images = extract_images_from_html(response.text, url)  # Extract images from HTML, passing base URL
    return jsonify({'images': images})
  except requests.exceptions.RequestException as e:
    return jsonify({'error': str(e)}), 500  # Internal Server Error

if __name__ == '__main__':
  app.run(debug=True)
