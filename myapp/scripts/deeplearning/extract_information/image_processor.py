from PIL import Image
import os
from extract_information.box_converter import BoxConverter
class ImageProcessor:

    def crop_and_save(self, image_path, box, box_index):
        """
        Crop the image using the PIL box coordinates and save it.

        :param image_path: Path to the original image
        :param box: EasyOCR box format [top-left, top-right, bottom-right, bottom-left]
        :param box_index: Index of the box (used for naming the cropped image file)
        :return: Path to the cropped image
        """
        image = Image.open(image_path)
        path =  f"myapp/static/cropped_images/{box_index}.png"
        pil_box = BoxConverter.convert_box_to_pil_box(box)
        cropped_image = image.crop(pil_box)
        cropped_image.save(path)
        return path
