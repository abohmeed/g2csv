import json
import requests
from bs4 import BeautifulSoup
import urllib
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def main(event,context):    
    response = []
    r = requests.get("https://www.google.com/search?q=" + event['keyword'])
    logging.info("Successfully contacted Google.com")
    bs = BeautifulSoup(r.text, features="html.parser")
    for link in bs.find_all('div', {'class': 'g'}):
        title = link.find('a')
        url = link.find('cite')
        if title and url:
            logging.info("Parsed %s", title.text)
            response.append({'title':title.text,'url':url.text})
    return json.dumps(response,sort_keys=True, indent=4)

event = json.loads('{"keyword":"docker"}')
# # print type(event)
main(event,"")