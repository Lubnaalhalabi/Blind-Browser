import math
from bs4 import BeautifulSoup
from pywebcopy import save_webpage
import os, sys
import json, time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse


class HTMLParser:
    def __init__(self, html_path,state):
        self.html_path = html_path
        self.soup = None
        self.zones = []
        self.n_list_dom = 0
        self.tagSpa = []
        self.state = state

    # Parse the saved HTML and clean up the DOM
    def parse(self):
        with open(self.html_path, 'r', encoding="utf-8") as f:
            soup = BeautifulSoup(f, 'html.parser')
        self.soup = soup
        # Remove unwanted p tags
        for p_tag in soup.findAll('p'):
            if len(str.strip(p_tag.text)) == 1 and ord(str.strip(p_tag.text)[0]) == 65279:
                p_tag.extract()
        if self.state == "all":
            # Find all tags in the HTML
            self.zones = soup.find_all(True, recursive=True)
        elif self.state == "child_of_body": 
            # Find zones in the body of the HTML
            self.zones = soup.find("body").findChildren(recursive=False)
        self.n_list_dom = len(self.zones)
        self.tagSpa = self.extract_nodes(self.zones)
        return self.tagSpa ,self.n_list_dom, self.soup
   
    # Extract nodes with their bounding box information
    def extract_nodes(self, zones):
        tagSpa = []
        for zone in zones:
            if zone.get('data-cleaned') or not zone.get('data-bbox'):
                self.n_list_dom -= 1
                continue
            boundingVal = zone.get('data-bbox').split()
            if self.state == "child_of_body":
                tagSpa.append({
                    len(tagSpa): {
                        'tagName': zone.name,
                        'x': float(boundingVal[0]),
                        'y': float(boundingVal[1]),
                        'width': float(boundingVal[2]),
                        'height': float(boundingVal[3]),
                        'space': float(boundingVal[4]),
                        'xCentre': float(boundingVal[0]) + float(boundingVal[2]) / 2,
                        'yCentre': float(boundingVal[1]) + float(boundingVal[3]) / 2,
                        'text': zone.text,
                        'seg': "true",
                        'xPath': zone.get('data-xpath')
                    }
                })
            elif self.state == "all":
                block_2_content = []  
                data_block = zone.get('data-block')
                if data_block and (data_block == "2" or data_block == "1" or data_block == "2 1"):
                    block_2_content.append(zone)
                    boundingVal = zone.get('data-bbox').split()
                    tagSpa.append({
                        len(tagSpa): {
                            'tagName': zone.name,
                            'x': float(boundingVal[0]),
                            'y': float(boundingVal[1]),
                            'width': float(boundingVal[2]),
                            'height': float(boundingVal[3]),
                            'space': float(boundingVal[4]),
                            'xCentre': float(boundingVal[0]) + float(boundingVal[2]) / 2,
                            'yCentre': float(boundingVal[1]) + float(boundingVal[3]) / 2,
                            'text': zone.text,
                            'seg': "true",
                            'xPath': zone.get('data-xpath')
                        }
                    })
        return tagSpa
