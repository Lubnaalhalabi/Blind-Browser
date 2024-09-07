from vision_based_algorithm.web_scraper import WebScraper
from vision_based_algorithm.script_injector import ScriptInjector
from vision_based_algorithm.html_parser import HTMLParser
from vision_based_algorithm.segmentation import Segmentation
from vision_based_algorithm.json_converter import JSONConverter
from vision_based_algorithm.border_drawer import BorderDrawer
import time
from urllib.parse import urlparse
import logging


# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class WebPageSegmentation:
    def __init__(self, driver, url,  n_zone, max_iter, html_url=" ",html_path=" ", saving = True,saving_json_path="vision_based_algorithm/clustersjson",isExist=False):
        self.driver = driver
        self.url = url
        self.n_zone = n_zone
        self.html_url = html_url
        self.saving = saving
        self.html_path = html_path
        self.max_iter = max_iter
        self.isExist = isExist 
        self.saving_json_path = saving_json_path

    # Main function to perform clustering on the given URL
    def clustering(self):  
        parsed_url = urlparse(self.url)
        domain = parsed_url.netloc
        # Scrape the webpage
        web_scraper = WebScraper(self.driver, self.url, domain)

        if self.saving and not self.isExist:
            html_path , html_url = web_scraper.save_full_html()
            self.driver.get(html_url)
            time.sleep(3)
            # Inject necessary scripts
            script_injector = ScriptInjector(self.driver,html_path)
            script_injector.inject_scripts()
        elif not self.saving and not self.isExist:
            self.driver.get(self.url)
            time.sleep(3)
            # Inject necessary scripts
            script_injector = ScriptInjector(self.driver,"")
            script_injector.inject_scripts()
            html_path , html_url = web_scraper.save_html()        
        elif self.isExist:
            self.driver.get(self.html_url)
            time.sleep(5)
            html_path = self.html_path
            html_url = self.html_url
            
            script_injector = ScriptInjector(self.driver,html_path)
            script_injector.inject_scripts()
            
            if not self.url =="":
                parts = self.url.split("/")
                domain = parts[1]
            else:                 
                parts = html_url.split("/")
                # Find the part containing the directory name
                directory_part = parts[-1]
                # Split the directory part by "\" or "/"
                directory_parts = directory_part.split("\\") if "\\" in directory_part else directory_part.split("/")
                # Extract the directory name
                domain = directory_parts[-2]
        logging.debug("HTML path and URL obtained.")
        # Parse the HTML and extract nodes
        html_parser = HTMLParser(html_path,"child_of_body")
        tagSpa, n_list_dom , soup = html_parser.parse()
        logging.debug("HTML parsed successfully.")
        # Perform segmentation
        segmentation = Segmentation(tagSpa,n_list_dom, soup)
        zon = segmentation.segmentation(self.n_zone, self.max_iter)
        logging.debug("Segmentation completed.")
        # Convert clustered zones to JSON
        json_converter = JSONConverter(zon, domain,self.saving_json_path)
        json_converter.convert_to_json()
        logging.debug("JSON conversion completed.")

        # Draw border around clustered zones
        border_drawer = BorderDrawer(self.driver, html_path, zon)
        border_drawer.draw_border()

        logging.debug("Border drawing completed.")
