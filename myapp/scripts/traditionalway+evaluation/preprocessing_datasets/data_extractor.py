import time
from vision_based_algorithm.script_injector import ScriptInjector
from vision_based_algorithm.html_parser import HTMLParser
from vision_based_algorithm.json_converter import JSONConverter

class DataExtractor:
    def __init__(self, driver, html_path, html_url, domain,saving_path):
        self.driver = driver
        self.html_path = html_path
        self.html_url = html_url
        self.domain = domain
        self.saving_path = saving_path

    def extract(self):
        self.driver.get(self.html_url)
        time.sleep(2)
        
        # Inject scripts
        injector = ScriptInjector(self.driver, self.html_path)
        injector.inject_scripts()
        
        # Parse HTML and clean up DOM
        parser = HTMLParser(self.html_path,"all")
        tagSpa, _, _ = parser.parse()
        
        # Convert to JSON
        converter = JSONConverter(tagSpa, self.domain, self.saving_path)
        converter.convert_to_json()

