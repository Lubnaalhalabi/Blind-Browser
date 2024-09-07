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

class BorderDrawer:
    def __init__(self, driver, html_path, zon):
        self.driver = driver
        self.html_path = html_path
        self.zon = zon

    # Draw border around clustered zones
    def draw_border(self):
        left = []
        top = []
        width = []
        height = []
        path = []
        for i in range(0, len(self.zon)):
            if self.zon[i][i]['tagName'] != "":
                left.append(self.zon[i][i]['x'])
                top.append(self.zon[i][i]['y'])
                width.append(self.zon[i][i]['width'])
                height.append(self.zon[i][i]['height'])
                path.append(self.zon[i][i]["xPath"])
        self.driver.execute_script(open("myapp/scripts/traditionalway+evaluation/vision_based_algorithm/js/drawBorder.js").read(), left, top, width, height, path)
        html_code = self.driver.page_source    
        with open(self.html_path, 'w', encoding="utf-8") as f:
            f.write(html_code)
