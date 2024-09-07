from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from vision_based_algorithm.web_page_segmentation import WebPageSegmentation
import sys , json , time
from screen_shot_fetcher import ScreenshotFetcher
import logging
from extract_information_tr.json_saver import JSONSaver
from extract_information_tr.processor import Processor



# Configure logging to output debug information
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    
    # Number of iterations for clustering
    numberitterations = 10000        

    # Get command line arguments
    # URL to capture screenshot and analyze
    url =  sys.argv[1]
    # Number of clusters for segmentation
    num_clusters = int(sys.argv[2])
    # Browser driver to use (chrome, firefox, edge)
    driver_name = sys.argv[3]    
  
    # Type of sumarization
    sumarize = sys.argv[4]


    # API key for screenshot fetching
    api_key = "c99fb63722944f579bc1de5fe4aea818"

    # Fetch screenshot from the provided URL using ScreenshotFetcher
    fetcher = ScreenshotFetcher(api_key)
    orginal_image = fetcher.fetch_screenshot(url)

    # Initialize the WebDriver based on the specified browser driver
    if driver_name == 'chrome':
        options = ChromeOptions()
        driver = webdriver.Chrome(options=options)
    elif driver_name == 'firefox':
        options = FirefoxOptions()
        driver = webdriver.Firefox(options=options)
    elif driver_name == 'edge':
        options = EdgeOptions()
        driver = webdriver.Edge(options=options)
    else:
        raise ValueError("Unsupported driver: {}".format(driver_name))
    
    # Maximize the browser window
    driver.maximize_window()
    
    # Path to save the JSON results
    json_path = "myapp/static/json_result_tr/results.json"

    # Initialize WebPageSegmentation with required parameters
    page_segmentation = WebPageSegmentation(driver,url, num_clusters, numberitterations,"","",False,json_path,False)

    # Perform page segmentation and clustering
    page_segmentation.clustering()
    logging.info("Clustering completed")
    
    # Close the browser window
    page_segmentation.driver.quit()

    # Load the JSON results from the file
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Initialize the Processor and process the image and data
    processor_ = Processor()
    results = processor_.process_image(orginal_image, data ,sumarize)
    
    # Save the results to a JSON file
    JSONSaver.save_results_to_json(results, json_path)

