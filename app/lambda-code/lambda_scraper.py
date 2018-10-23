import json
import requests
from bs4 import BeautifulSoup
import logging
import boto3
import csv

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
    return response
    

def main(event,context):    
    logger.info(event)
    keywords = event["Records"][0]["sns"]["message"]["keywords"]
    result = scrape(keywords)
    with open('/tmp/keywords.csv', 'wb') as f:
        w = csv.DictWriter(f, result[0].keys())
        w.writeheader()
        w.writerows(result)
    s3 = boto3.client('s3')
    s3.upload_file('/tmp/keywords.csv', 'gscraper.downloads/' + + '.csv")


# event = {u'Records': [{u'eventVersion': u'2.0', u'eventTime': u'2018-10-18T14:07:00.676Z', u'requestParameters': {u'sourceIPAddress': u'41.33.59.145'}, u's3': {u'configurationId': u'895e0457-7b21-48af-a6b7-70bda7d48e7c', u'object': {u'eTag': u'512278359caf9bcdeee50a98d813ed42', u'sequencer': u'005BC89384A152327E', u'key': u'keywords.txt', u'size': 26}, u'bucket': {u'arn': u'arn:aws:s3:::gscraper.uploads', u'name': u'gscraper.uploads', u'ownerIdentity': {u'principalId': u'A2AHDBAACARLZN'}}, u's3SchemaVersion': u'1.0'}, u'responseElements': {u'x-amz-id-2': u'E5HHXp/5RdzELVyxKKzeoTaozIdo0nrpoGP4BYsxzBBBN8GFH0Ya1HoFrGrZOMSSMzBiTVRcYY8=', u'x-amz-request-id': u'F93C166AFB381653'}, u'awsRegion': u'us-west-2', u'eventName': u'ObjectCreated:Put', u'userIdentity': {u'principalId': u'A2AHDBAACARLZN'}, u'eventSource': u'aws:s3'}]}
# main(event,"")