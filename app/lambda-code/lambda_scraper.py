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
    content = json.loads(event["Records"][0]["Sns"]["Message"])
    keywords = content["keywords"]
    key = content["key"]
    result = scrape(keywords)
    with open('/tmp/keywords.csv', 'wb') as f:
        w = csv.DictWriter(f, result[0].keys())
        w.writeheader()
        w.writerows(result)
    s3 = boto3.client('s3')
    s3.upload_file('/tmp/keywords.csv', 'g2csv.downloads',key + '.csv')


event = {u'Records': [{u'EventVersion': u'1.0', u'EventSubscriptionArn': u'arn:aws:sns:us-west-2:790250078024:keywords:65d007c1-9d37-407d-bd7a-eee88a85e99e', u'EventSource': u'aws:sns', u'Sns': {u'SignatureVersion': u'1', u'Timestamp': u'2018-10-23T15:06:12.362Z', u'Signature': u'SOfT0TdBvOLgo6HXzlgkA5W4ckrtwVYV1xUm+BU6x8fDqWp1xQnhK311Y6DbekCjuzzz+lRn6JwVr28Ey9VwLcy3k3GVEMInRtkWjLs5iEJm1nbCWB8oUOD01TuHIlXDJw4HIjvRDVox6CAX3AZIcROOF8ndnerd9BdFw20DfIHHZ56DJ8XI7S2Y2j/K2h611xFOaWc8rkzZNWW2mYShmJgROfhngjiMgLfdVvc1vT5UvvoFok6Kp3h2BZ5pfmYbPac6zJVw+ubjJGQVkJfMY9djyanrfImukbibJbMfPrGGg40K3elRguPPXOuRgStlgxV7EqUL+p6QkLpXaRHUfQ==', u'SigningCertUrl': u'https://sns.us-west-2.amazonaws.com/SimpleNotificationService-ac565b8b1a6c5d002d285f9598aa1d9b.pem', u'MessageId': u'1b6e4d58-a839-5553-9f29-1911931de346', u'Message': u'{"keywords": ["simple", "notification", "service"], "key": "92ec54c02926b1d851da14084d01995ae3127920c8882b2f51df39a4"}', u'MessageAttributes': {}, u'Type': u'Notification', u'UnsubscribeUrl': u'https://sns.us-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-west-2:790250078024:keywords:65d007c1-9d37-407d-bd7a-eee88a85e99e', u'TopicArn': u'arn:aws:sns:us-west-2:790250078024:keywords', u'Subject': u'Test'}}]}
main(event,"")