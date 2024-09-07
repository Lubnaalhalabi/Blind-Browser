# Class to fetch screenshots of web pages using an API
import requests
from PIL import Image
import numpy as np
import cv2
import io

class ScreenshotFetcher:
    def __init__(self, api_key):
        """
        Initialize the ScreenshotFetcher with an API key.

        Parameters:
        api_key (str): The API key for accessing the screenshot service.
        """
        self.api_key = api_key

    def fetch_screenshot(self, url):
        """
        Fetch a screenshot of a web page.

        Parameters:
        url (str): The URL of the web page to capture.

        Returns:
        numpy.ndarray or None: The screenshot image in RGB format as a NumPy array,
        or None if the request fails.
        """
        # Construct the API URL with the provided API key and target URL
        api_url = f"https://api.apiflash.com/v1/urltoimage?access_key={self.api_key}&url={url}&full_page=true"

        # Make a GET request to the API
        response = requests.get(api_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Load the image from the response content
            image = Image.open(io.BytesIO(response.content))

            # Convert the image to a NumPy array
            image_np = np.array(image)

            # Convert the image from BGR to RGB format
            image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)

            # Return the RGB image
            return image_rgb
        else:
            # Print an error message if the request failed
            print(f"Failed to fetch screenshot. Status code: {response.status_code}")
            return None