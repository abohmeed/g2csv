import requests
from bs4 import BeautifulSoup
#TODO: add API functionality to the file
#TODO: convert the search query to be URL-friendly


r = requests.get("https://www.google.com/search?q=beautifulsoup")
bs = BeautifulSoup(r.text,features="html.parser")

for link in bs.find_all('div',{'class':'g'}):
    title = link.find('a')
    url = link.find('cite')
    if title and url:
        print title.text, url.text