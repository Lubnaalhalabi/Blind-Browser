from segmentation.main_processor import MainProcessor
import sys
    
def main(url):
    # List of URLs to process
    url =  sys.argv[1]

    # API key for screenshot fetching service
    api_key = "c99fb63722944f579bc1de5fe4aea818"

    # Checkpoint for SAM model
    checkpoint = "sam_vit_h_4b8939.pth"

    # Initialize MainProcessor for the current URL
    processor = MainProcessor(url, api_key, checkpoint)
    
    # Process the URL to segment paragraphs and get results
    number_of_cluster, final_boxes = processor.process()
    return number_of_cluster

if __name__ == "__main__":
    url = sys.argv[1]
    result = main(url)
    print(result)
