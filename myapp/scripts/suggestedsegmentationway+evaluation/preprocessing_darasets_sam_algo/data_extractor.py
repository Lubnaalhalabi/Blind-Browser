import time
from preprocessing_darasets_sam_algo.mapping import HTMLParser
from preprocessing_darasets_sam_algo.json_converter import JSONConverter

class DataExtractor:
    def __init__(self, driver, html_path, html_url, domain,saving_path,box):
        self.driver = driver
        self.html_path = html_path
        self.html_url = html_url
        self.domain = domain
        self.saving_path = saving_path
        self.box = box

    def extract(self):
        self.driver.get(self.html_url)
        time.sleep(2)
        
        # Parse HTML and clean up DOM
        parser = HTMLParser(self.html_path,"all", self.box)
        tagSpa, _, _ = parser.parse()
        
        # Convert to JSON
        converter = JSONConverter(tagSpa, self.domain, self.saving_path)
        converter.convert_to_json()

