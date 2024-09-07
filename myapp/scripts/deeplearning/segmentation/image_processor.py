import cv2,os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.cluster.hierarchy import fclusterdata
# Class to process an image and segment it into paragraphs using bounding boxes
class ImageProcessor:
    def __init__(self, saving_orginal_image_path, mask_image):
        """
        Initialize the ImageProcessor with the image and mask image.

        Parameters:
        image (numpy.ndarray): The original input image.
        mask_image (numpy.ndarray): The mask image for segmentation.
        """
        self.mask_image = mask_image
        self.image =cv2.imread(saving_orginal_image_path)
        self.base_path = os.path.join(os.path.dirname(__file__), '..', 'results')



    def process_image(self):
        """
        Process the image to find and draw bounding boxes around paragraphs.

        Returns:
        list: A list of final bounding boxes.
        """
        if self.image is None:
            raise ValueError("Failed to load image from the input")

        # Ensure mask_image has the correct data type and number of channels
        if self.mask_image.dtype != np.uint8:
            self.mask_image = (self.mask_image * 255).astype(np.uint8)

        if len(self.mask_image.shape) == 2:  # Grayscale image
            self.mask_image = cv2.cvtColor(self.mask_image, cv2.COLOR_GRAY2BGR)
        elif self.mask_image.shape[2] == 4:  # BGRA image
            self.mask_image = cv2.cvtColor(self.mask_image, cv2.COLOR_BGRA2BGR)

        # Convert mask_image to grayscale
        gray_image = cv2.cvtColor(self.mask_image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to the grayscale image
        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)


        # Perform edge detection using Canny
        edges = cv2.Canny(blurred_image, 50, 150)


        # Find contours in the edge-detected image
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Calculate bounding boxes for each contour
        bounding_boxes = [cv2.boundingRect(contour) for contour in contours]


        bounding_boxes_array = np.array(bounding_boxes)

        # Cluster bounding boxes based on distance threshold
        threshold_distance = 50  # Adjust this threshold based on your image
        clusters = fclusterdata(bounding_boxes_array, t=threshold_distance, criterion="distance")

        # Group bounding boxes by clusters and merge them
        grouped_boxes = []
        for cluster_id in np.unique(clusters):
            cluster_boxes = bounding_boxes_array[clusters == cluster_id]
            merged_box = self.merge_bounding_boxes(cluster_boxes)
            grouped_boxes.append(merged_box)

        # Filter out inner boxes
        filtered_boxes = self.filter_inner_boxes(grouped_boxes)

        # Merge overlapping boxes
        final_boxes = self.merge_overlapping_boxes(filtered_boxes)

        # Draw bounding boxes around each paragraph
        segmented_image = self.image.copy()
        for box in final_boxes:
            x, y, w, h = box
            cv2.rectangle(segmented_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Display the segmented image
        plt.figure(figsize=(75, 75))
        plt.imshow(segmented_image)
        plt.axis('off')
        plt.savefig(os.path.join(self.base_path, "segmented_image.png"))
        # plt.show()
        plt.close()
        segmented_image = np.array(segmented_image)
        segmented_image_pil = Image.fromarray(segmented_image)
        segmented_image_pil.save("myapp/static/Images/segmented_image.png")
        return final_boxes


    def merge_bounding_boxes(self, boxes):
        """
        Merge multiple bounding boxes into a single bounding box.

        Parameters:
        boxes (list): List of bounding boxes to be merged.

        Returns:
        tuple: A single bounding box that encompasses all input boxes.
        """
        x_min = min([box[0] for box in boxes])
        y_min = min([box[1] for box in boxes])
        x_max = max([box[0] + box[2] for box in boxes])
        y_max = max([box[1] + box[3] for box in boxes])
        return (x_min, y_min, x_max - x_min, y_max - y_min)

    def filter_inner_boxes(self, boxes, tolerance=0.1):
        """
        Filter out boxes that are within other boxes.

        Parameters:
        boxes (list): List of bounding boxes.
        tolerance (float): Tolerance for considering a box within another. Default is 0.1.

        Returns:
        list: Filtered list of bounding boxes.
        """
        filtered_boxes = []
        for i, box in enumerate(boxes):
            x, y, w, h = box
            outer_box = False
            for j, other_box in enumerate(boxes):
                if i != j:
                    ox, oy, ow, oh = other_box
                    # Expand the other_box boundaries by tolerance
                    ox_min = ox - tolerance
                    oy_min = oy - tolerance
                    ox_max = ox + ow + tolerance
                    oy_max = oy + oh + tolerance

                    # Check if box is within other_box with tolerance
                    if x >= ox_min and y >= oy_min and x + w <= ox_max and y + h <= oy_max:
                        outer_box = True
                        break
            if not outer_box:
                filtered_boxes.append(box)
        return filtered_boxes

    def merge_overlapping_boxes(self, boxes, overlap_threshold=0.01):
        """
        Merge overlapping bounding boxes into larger boxes.

        Parameters:
        boxes (list): List of bounding boxes.
        overlap_threshold (float): Threshold for considering boxes as overlapping. Default is 0.01.

        Returns:
        list: List of merged bounding boxes.
        """
        def overlap_area(box1, box2):
            """
            Calculate the overlap area between two boxes.

            Parameters:
            box1 (tuple): The first bounding box.
            box2 (tuple): The second bounding box.

            Returns:
            float: The overlap area as a fraction of the union area of the two boxes.
            """
            x1, y1, w1, h1 = box1
            x2, y2, w2, h2 = box2

            x_overlap = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
            y_overlap = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
            overlap = x_overlap * y_overlap
            area1 = w1 * h1
            area2 = w2 * h2

            return overlap / float(area1 + area2 - overlap)

        def merge_boxes(box1, box2):
            """
            Merge two bounding boxes into a single bounding box.

            Parameters:
            box1 (tuple): The first bounding box.
            box2 (tuple): The second bounding box.

            Returns:
            tuple: The merged bounding box.
            """
            x_min = min(box1[0], box2[0])
            y_min = min(box1[1], box2[1])
            x_max = max(box1[0] + box1[2], box2[0] + box2[2])
            y_max = max(box1[1] + box1[3], box2[1] + box2[3])
            return (x_min, y_min, x_max - x_min, y_max - y_min)

        # Function to check if a box overlaps with any box in the merged list
        def does_overlap_with_any(box, merged_boxes):
            """
            Check if a box overlaps with any box in the list of merged boxes.

            Parameters:
            box (tuple): The bounding box to check.
            merged_boxes (list): The list of merged bounding boxes.

            Returns:
            bool: True if the box overlaps with any box in the merged list, False otherwise.
            """
            for merged_box in merged_boxes:
                if overlap_area(box, merged_box) > overlap_threshold:
                    return True
            return False

        merged_boxes = []

        # Sort boxes by their y-coordinate to process from top to bottom
        boxes_sorted = sorted(boxes, key=lambda box: box[1])

        for box in boxes_sorted:
            if not does_overlap_with_any(box, merged_boxes):
                merged_boxes.append(box)
            else:
                # If the box overlaps with existing merged boxes, merge them together
                overlapping_boxes = [merged_box for merged_box in merged_boxes if overlap_area(box, merged_box) > overlap_threshold]
                merged_box = box
                for overlapping_box in overlapping_boxes:
                    merged_box = merge_boxes(merged_box, overlapping_box)
                merged_boxes = [mb for mb in merged_boxes if mb not in overlapping_boxes]
                merged_boxes.append(merged_box)

        return merged_boxes
