import gc
import numpy as np
import matplotlib.pyplot as plt
import os
import numpy as np
from screen_shot_fetcher import ScreenshotFetcher
from sam2_test import Sam2

class MainProcessor:
    def __init__(self, url, api_key):
        """
        Initialize the MainProcessor with the given URL, API key, and checkpoint.

        Parameters:
        url (str): The URL of the web page to fetch.
        api_key (str): The API key for the screenshot service.
        """
        self.url = url
        self.api_key = api_key
        self.base_path = os.path.join(os.path.dirname(__file__), '..', 'results')

    
    def process(self):
        """
        Process the web page to segment paragraphs and return the number of clusters and final bounding boxes.
        """
        # Define the path where the original screenshot will be saved
        saving_orginal_image_path = os.path.join(self.base_path, "Original.png")

        # Step 1: Fetch the screenshot
        fetcher = ScreenshotFetcher(self.api_key)
        image = fetcher.fetch_screenshot(self.url)

        # Save the fetched screenshot to the defined path        
        plt.figure(figsize=(20, 30))
        plt.imshow(image)
        plt.axis('off')
        plt.savefig(saving_orginal_image_path)
        plt.close()

        # Step 2: Perform image segmentation
        segmentor = Sam2(saving_orginal_image_path)
        segmentor.segment()
        
if __name__ == "__main__":
    
    # Define the URL and API key for fetching the screenshot
    url =  "https://sider.ai/apps/lp-chatgpt?source=gg&p1=ainew19&p2=search&gad_source=5&gclid=EAIaIQobChMIvdCjudPXhwMVbpNQBh0LxwcmEAAYAiAAEgKjZPD_BwE"
    api_key = "c99fb63722944f579bc1de5fe4aea818"
    
    # Create an instance of MainProcessor and process the image
    processor = MainProcessor(url, api_key)
    processor.process()