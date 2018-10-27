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


@app.route('/send', methods=['POST'])
def index():
    content = request.json
    key = hashlib.sha224(str(content)).hexdigest()
    message = {"keywords": content['keywords'], "key": key}
    json_message = json.dumps({"default": json.dumps(message)})
    client = boto3.client('sns')
    try:
        response = client.publish(
            TopicArn="arn:aws:sns:us-west-2:790250078024:keywords",
            Message=json_message,
            Subject="Test",
            MessageStructure="json"
        )
        return jsonify({"Response": response,"Key":key, "Success":"True"})
    except Exception as e:
        return jsonify({"Response": str(e),"Success":"False"})

    return json_message
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
