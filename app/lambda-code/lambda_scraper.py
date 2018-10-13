import json
import requests
from bs4 import BeautifulSoup
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def scrape(keywords):
    logger.info(keywords)
    response = []
    for k in keywords:
        logger.info("Parsing "+k)
        r = requests.get("https://www.google.com/search?q=" + k)
        logging.info("Successfully contacted Google.com")
        bs = BeautifulSoup(r.text, features="html.parser")
        for link in bs.find_all('div', {'class': 'g'}):
            title = link.find('a')
            url = link.find('cite')
            if title and url:
                logging.info("Parsed %s", title.text)
                response.append({'keyword':k,'title':title.text,'url':url.text})
    return json.dumps(response,sort_keys=True, indent=4)

def main(event,context):    
    logger.info(event)
    key = event["Records"][0]["s3"]["object"]["key"]
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    s3 = boto3.resource('s3')
    s3.Object(bucket,key).download_file('/tmp/keywords.txt')
    with open('/tmp/keywords.txt') as f:
        lines = [line.rstrip('\n') for line in f]
    result = scrape(lines)
    with open('/tmp/keywords.json', 'w') as f:
        f.write(result)
    s3 = boto3.client('s3')
    s3.upload_file('/tmp/keywords.json', 'gscraper.downloads', key + ".json")


# event = {u'Records': [{u'eventVersion': u'2.0', u'eventTime': u'2018-10-13T11:49:42.272Z', u'requestParameters': {u'sourceIPAddress': u'156.197.36.206'}, u's3': {u'configurationId': u'035518bf-df9b-4fb7-bafa-227bef9d7793', u'object': {u'eTag': u'04e44f2d78b56ff4de6a09fa7694f0e3', u'sequencer': u'005BC1DBD63BC17945', u'key': u'Keywords.txt', u'size': 19}, u'bucket': {u'arn': u'arn:aws:s3:::gscraper.uploads', u'name': u'gscraper.uploads', u'ownerIdentity': {u'principalId': u'A2AHDBAACARLZN'}}, u's3SchemaVersion': u'1.0'}, u'responseElements': {u'x-amz-id-2': u'uQhECxvKRsFdytmpCWG1W49MIPcx3EmwIUkAzCmqXWqaegUzJExpt8xWTwmISZW78qoLvVS2gfI=', u'x-amz-request-id': u'806D4BCED136AC00'}, u'awsRegion': u'us-west-2', u'eventName': u'ObjectCreated:Put', u'userIdentity': {u'principalId': u'A2AHDBAACARLZN'}, u'eventSource': u'aws:s3'}]}
# main(event,"")