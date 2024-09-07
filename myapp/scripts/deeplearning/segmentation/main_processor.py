import gc
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from skimage.filters import threshold_local

from segmentation.screen_shot_fetcher import ScreenshotFetcher
from segmentation.edge_detector import EdgeDetector
from segmentation.clustering import Clustering
from segmentation.sam_segmentation import SamSegmentation
from segmentation.mathematical_morphology import MathematicalMorphology
from segmentation.image_processor import ImageProcessor

class MainProcessor:
    def __init__(self, url, api_key, checkpoint):
        """
        Initialize the MainProcessor with the given URL, API key, and checkpoint.

        Parameters:
        url (str): The URL of the web page to fetch.
        api_key (str): The API key for the screenshot service.
        checkpoint (str): The checkpoint for the SAM model.
        """
        self.url = url
        self.api_key = api_key
        self.checkpoint = checkpoint
        self.base_path = os.path.join(os.path.dirname(__file__), '..', 'results')


    def process(self):
        """
        Process the web page to segment paragraphs and return the number of clusters and final bounding boxes.

        Returns:
        tuple: A tuple containing the number of clusters and the final bounding boxes.
        """
        saving_orginal_image_path = os.path.join(self.base_path, "Original.png")

        # Step 1: Fetch screenshot
        fetcher = ScreenshotFetcher(self.api_key)
        image = fetcher.fetch_screenshot(self.url)
        plt.figure(figsize=(75, 75))
        plt.imshow(image)
        plt.axis('off')
        plt.savefig(saving_orginal_image_path)
        # plt.show() 
        plt.close()
        # Step 2: Edge detection and contour extraction
        edge_detector = EdgeDetector()
        edges = edge_detector.detect_edges(image)
        contours = edge_detector.find_contours(edges)
        centroids = edge_detector.extract_centroids(contours)

        # Step 3: Clustering
        clustering = Clustering()
        _, cluster_centers = clustering.perform_clustering(centroids, eps=10, min_samples=2)

        # Step 4: SAM Segmentation
        sam_segmentation = SamSegmentation(self.checkpoint)
        onnx_model_path = "sam_onnx_example.onnx"
        if not os.path.exists(onnx_model_path):
            sam_segmentation.export_to_onnx(onnx_model_path)
        sam_segmentation.load_onnx_model(onnx_model_path)

        saving_segmented_image_path = os.path.join(self.base_path, "sam_segmented_image.png")

        # Step 5: Preprocessing
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        adaptive_thresh = threshold_local(gray_image, block_size=91, offset=5)
        binary_image = (gray_image > adaptive_thresh).astype(np.uint8) * 255
        res = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2RGB)

        # Step 6: Segment the image using SAM and show results
        masks = sam_segmentation.segment_image(res, cluster_centers)
        sam_segmentation.show_results(image, masks, cluster_centers, saving_segmented_image_path)

        # Step 7: Calculate the remaining clusters after segmentation
        _, number_of_cluster = sam_segmentation.calculate_remaining_clusters(masks)

        # Step 8: Apply mathematical morphology to the segmented image
        morph_processor = MathematicalMorphology(saving_segmented_image_path)
        filled_image = morph_processor.apply_morphology()


        # Step 9: Load the original image and process it to find final bounding boxes
        image_processor = ImageProcessor(saving_orginal_image_path, filled_image)
        final_boxes = image_processor.process_image()

        # Step 10: Clean up resources
        del edges, contours, centroids, cluster_centers, masks
        gc.collect()

        return number_of_cluster, final_boxes
