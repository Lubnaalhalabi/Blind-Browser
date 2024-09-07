import cv2
import numpy as np
from skimage.filters import threshold_local
# Class for applying mathematical morphology operations on an image
class MathematicalMorphology:
    def __init__(self, image_path):
        """
        Initialize the MathematicalMorphology with the path to an image.

        Parameters:
        image_path (str): The file path to the input image.
        """
        self.image_path = image_path
        self.image = cv2.imread(self.image_path)  # Read the image from the file path

    def apply_morphology(self):
        """
        Apply morphological operations to the input image to fill holes and remove noise.

        Returns:
        numpy.ndarray: The processed image after morphological operations.
        """
        # Convert the image to grayscale
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Use adaptive thresholding for binarization
        adaptive_thresh = threshold_local(gray_image, block_size=91, offset=5)
        binary_image = (gray_image > adaptive_thresh).astype(np.uint8) * 255

        # Create a kernel for morphological operations
        kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        kernel_open = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

        # Apply the morphological close operation to fill small holes

        opened_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel_open, iterations=1)

        closed_image = cv2.morphologyEx(opened_image, cv2.MORPH_CLOSE, kernel_close, iterations=2)

        # Invert the colors of the closed image
        inverted_image = cv2.bitwise_not(opened_image)

        # Copy the inverted image for flood filling
        flood_filled_image = inverted_image.copy()

        # Get the dimensions of the inverted image
        h, w = inverted_image.shape

        # Create a mask for flood filling (note the mask size is 2 pixels larger than the image)
        mask = np.zeros((h+2, w+2), np.uint8)

        # Apply flood fill starting from the top-left corner (0, 0)
        cv2.floodFill(flood_filled_image, mask, (0, 0), 255)

        # Invert the flood-filled image
        flood_filled_image = cv2.bitwise_not(flood_filled_image)

        # Combine the original closed image with the flood-filled inverted image to fill holes
        filled_image = closed_image | flood_filled_image

        # Return the processed image
        return filled_image