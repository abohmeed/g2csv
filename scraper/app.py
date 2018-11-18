import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import request
from flask import jsonify
import urllib
import logging

app = Flask(__name__)
# TODO: convert the search query to be URL-friendly

logger = logging.getLogger()
logger.setLevel('INFO')
logging.basicConfig()

@app.route('/', methods=['POST'])
def index():
    response = []
    query = request.form['query']
    logger.info(query)
    r = requests.get("https://www.google.com/search?q=" + query)
    bs = BeautifulSoup(r.text, features="html.parser")
    for link in bs.find_all('div', {'class': 'g'}):
        title = link.find('a')
        url = link.find('cite')
        if title and url:
            response.append({'title':title.text,'url':url.text})
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
