from vision_based_algorithm.web_page_segmentation import WebPageSegmentation
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import csv
import os

class DataSegmenter:
    def __init__(self, csv_dataset_path, saving_json_path):
        self.csv_dataset_path = csv_dataset_path
        self.saving_json_path = saving_json_path

    def segment(self):
        number_iterations = 10000
        with open(self.csv_dataset_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                domain = row['domain']
                url = row['block_path']
                number_of_cluster = int(row['num_cluster'])
                
                current_dir = os.getcwd()
                html_path = os.path.join(current_dir, 'resources', url)
                html_url = f'file:///{html_path}'

                options = Options()
                options.headless = True
                driver = webdriver.Firefox(options=options)
                driver.maximize_window()

                page_segmentation = WebPageSegmentation(
                    driver, url,
                    number_of_cluster, number_iterations, 
                    html_url, html_path, 
                    False, self.saving_json_path, True
                )
                page_segmentation.clustering()
                page_segmentation.driver.quit()
