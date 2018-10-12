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
    logger.info(event)
    # return scrape(event['keywords'])    

event = json.loads('{"keywords":["docker","AWS"]}')
print main(event,"")