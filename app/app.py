import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import request
from flask import jsonify
import urllib
import boto3
import hashlib

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    response = []
    query = urllib.quote_plus(request.form['query'])
    key = hashlib.sha224(query).hexdigest()
    return query    

if __name__ == '__main__':
    app.run(debug=True)
