from segmentation.main_processor import MainProcessor
import os, sys
from extract_information.json_saver import JSONSaver
from extract_information.processor import Processor
if __name__ == "__main__":


    # List of URLs to process
    url =  sys.argv[1]

    # Type of sumarization
    sumarize = sys.argv[2]

    # API key for screenshot fetching service
    api_key = "c99fb63722944f579bc1de5fe4aea818"

    tesseract_cmd_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    base_path = os.path.join(os.path.dirname(__file__), 'results')

    image_path =  os.path.join(base_path, "Original.png")

    # Checkpoint for SAM model
    checkpoint = "sam_vit_h_4b8939.pth"

    # Initialize MainProcessor for the current URL
    processor = MainProcessor(url, api_key, checkpoint)
    
    # Process the URL to segment paragraphs and get results
    number_of_cluster, final_boxes = processor.process()

    # Initialize the Processor
    processor_ = Processor(tesseract_cmd=tesseract_cmd_path)

    # Process the image to extract text and summaries and audio
    results = processor_.process_image(image_path, final_boxes,sumarize)

    # Save the results to a JSON file
    json_filename = os.path.join(base_path, "results.json")
    JSONSaver.save_results_to_json(results, json_filename)
    output_file = "myapp/static/json_result/results.json"
    JSONSaver.save_results_to_json(results, output_file)

    # Print the number of clusters/masks found for the current URL
    print(f'Number of masks in {url}: {number_of_cluster}')