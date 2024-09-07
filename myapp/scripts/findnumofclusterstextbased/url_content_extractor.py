import requests
from bs4 import BeautifulSoup

# Class to extract content from URLs
class URLContentExtractor:
    def extract_text(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        tags = ['h1', 'h2', 'h3', 'p']
        texts = []
        for tag in tags:
            for element in soup.find_all(tag):
                texts.append(element.get_text())
        return texts