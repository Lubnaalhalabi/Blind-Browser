from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from preprocessing_darasets_sam_algo.data_extractor import DataExtractor
import csv
import os,json

class DataProcessor:
    def __init__(self, csv_dataset_path, saving_json_path):
        self.csv_dataset_path = csv_dataset_path
        self.saving_json_path = saving_json_path

    def process(self):
        with open(self.csv_dataset_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                domain = row['domain']
                url = row['block_path']
                box = row['Bounding_Boxes']
                
                try:
                    box_list = json.loads(box)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    continue

                current_dir = os.getcwd()
                html_path = os.path.join(current_dir, 'resources', url)
                html_url = f'file:///{html_path}'

                options = Options()
                options.headless = True
                driver = webdriver.Firefox(options=options)
                driver.maximize_window()

                process_data = DataExtractor(driver, html_path, html_url, domain, self.saving_json_path,box_list)
                process_data.extract()
                process_data.driver.quit()
