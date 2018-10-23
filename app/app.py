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
    # payload = {"default":keywords":content['keywords'],"key":key}
    message = {"keywords":content['keywords'],"key":key}
    json_message = json.dumps({"default":json.dumps(message)})
    client = boto3.client('sns')
    response = client.publish(
        TopicArn="arn:aws:sns:us-west-2:790250078024:keywords",
        Message=json_message,
        Subject="Test",
        MessageStructure="json"
    )
    return json_message

if __name__ == '__main__':
    app.run(debug=True)
