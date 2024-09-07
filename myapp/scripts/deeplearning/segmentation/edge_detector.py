import numpy as np
import cv2

# Class for edge detection and contour extraction
class EdgeDetector:
    def detect_edges(self, image):
        """
        Detect edges in an image using the Canny edge detection algorithm.

        Parameters:
        image (numpy.ndarray): The input image in which edges are to be detected.

        Returns:
        numpy.ndarray: The binary image with detected edges.
        """
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect edges using the Canny algorithm
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        # Return the image with detected edges
        return edges

    def find_contours(self, edges):
        """
        Find contours in a binary edge-detected image.

        Parameters:
        edges (numpy.ndarray): The binary image with detected edges.

        Returns:
        list: A list of detected contours.
        """
        # Find contours in the edge-detected image
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Return the list of contours
        return contours

    def extract_centroids(self, contours, min_area=10):
        """
        Extract the centroids of contours with an area larger than a specified minimum.

        Parameters:
        contours (list): A list of detected contours.
        min_area (int): The minimum area threshold for considering a contour.

        Returns:
        list: A list of centroids (x, y) of the contours that meet the area criteria.
        """
        centroids = []

        # Iterate over the contours
        for contour in contours:
            # Check if the contour area is greater than the minimum area
            if cv2.contourArea(contour) > min_area:
                # Calculate the moments of the contour
                M = cv2.moments(contour)

                # Calculate the centroid if the area (m00) is not zero
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    # Append the centroid coordinates to the list
                    centroids.append((cx, cy))

        # Return the list of centroids
        return centroids