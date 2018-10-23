import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import request
from flask import jsonify
import urllib
import boto3
import hashlib
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    content = request.json
    key = hashlib.sha224(str(content)).hexdigest()
    # return json.dumps(content)
    return content["keywords"][0]
    

if __name__ == '__main__':
    app.run(debug=True)
