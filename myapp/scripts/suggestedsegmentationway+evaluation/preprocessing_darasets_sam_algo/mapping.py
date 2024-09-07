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
    def __init__(self, html_path,state, box):
        self.html_path = html_path
        self.soup = None
        self.zones = []
        self.box = box
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
        self.n_list_dom = len(self.zones)
        self.tagSpa = self.extract_nodes(self.zones)
        return self.tagSpa ,self.n_list_dom, self.soup
   
    # Extract nodes with their bounding box information
    def extract_nodes(self, zones):
        tagSpa = []
        for b in self.box:
            for zone in zones:
                if zone.get('data-cleaned') or not zone.get('data-bbox'):
                    self.n_list_dom -= 1
                    continue
                boundingVal = zone.get('data-bbox').split()
                boundingVal = [float(val) for val in boundingVal]
                if self.state == "all":
                    block_2_content = []  
                    if boundingVal and (b[0]-0.1*b[0] <= boundingVal[0] <= b[0]+0.1*b[0]
                                        and
                                        b[1]-0.1*b[1] <= boundingVal[1] <= b[1]+0.1*b[1]
                                        or
                                        b[2]-0.1*b[2] <= boundingVal[2] <= b[2]+0.1*b[2]
                                        and
                                        b[3]-0.1*b[3] <= boundingVal[3] <= b[3]+0.1*b[3]                                        
                                        ):
                        block_2_content.append(zone)
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
                        break   
        return tagSpa
