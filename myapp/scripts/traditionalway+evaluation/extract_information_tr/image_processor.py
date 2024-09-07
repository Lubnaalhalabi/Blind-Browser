from PIL import Image
import os
import numpy as np
from extract_information_tr.box_converter import BoxConverter
class ImageProcessor:

    def crop_and_save(self, image, box, box_index):
        """
        Crop the image using the PIL box coordinates and save it.

        :param image_path: Path to the original image
        :param box: EasyOCR box format [top-left, top-right, bottom-right, bottom-left]
        :param box_index: Index of the box (used for naming the cropped image file)
        :return: Path to the cropped image
        """
        
        # Check if the image is a NumPy array
        if isinstance(image, np.ndarray):
            # Convert NumPy array to PIL Image
            if image.ndim == 3 and image.shape[2] == 3:
                pil_image = Image.fromarray(image, 'RGB')
            elif image.ndim == 2:
                pil_image = Image.fromarray(image, 'L')
            else:
                raise ValueError("Unsupported image array format")
        else:
            raise TypeError("Image must be a PIL Image or NumPy array")

        path =  f"myapp/static/cropped_images_tr/{box_index}.png"
        
        pil_box = BoxConverter.convert_box_to_pil_box(box)
        
        cropped_image = pil_image.crop(pil_box)
        
        cropped_image.save(path)
        
        return path
