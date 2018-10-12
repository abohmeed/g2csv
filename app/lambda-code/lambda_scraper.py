import json
import requests
from bs4 import BeautifulSoup
import urllib
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def scrape(keywords):
    response = []
    for k in event['keywords']:
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
    # logger.info(event)
    # return scrape(event['keywords'])    
    key = event["Records"][0]["s3"]["object"]["key"]
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    print "s3://" + bucket + "/" + key

event = {u'Records': [{u'eventVersion': u'2.0', u'eventTime': u'2018-10-10T14:31:14.736Z', u'requestParameters': {u'sourceIPAddress': u'41.33.59.145'}, u's3': {u'configurationId': u'035518bf-df9b-4fb7-bafa-227bef9d7793', u'object': {u'eTag': u'c680e919b86b379457a309f10da72376', u'sequencer': u'005BBE0D32A3A8E820', u'key': u'.bash_history', u'size': 183}, u'bucket': {u'arn': u'arn:aws:s3:::gscraper.uploads', u'name': u'gscraper.uploads', u'ownerIdentity': {u'principalId': u'A2AHDBAACARLZN'}}, u's3SchemaVersion': u'1.0'}, u'responseElements': {u'x-amz-id-2': u'PvX+43FiSZFMoaanCaS/lqP+ue9Y/3q/T3BwrMgHQPSHt4n4JLoAdbxA97xt1+JN6Lbo4zxqybw=', u'x-amz-request-id': u'341A81C199531AF7'}, u'awsRegion': u'us-west-2', u'eventName': u'ObjectCreated:Put', u'userIdentity': {u'principalId': u'A2AHDBAACARLZN'}, u'eventSource': u'aws:s3'}]}
main(event,"")