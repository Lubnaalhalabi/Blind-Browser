import pytesseract
from PIL import Image
from extract_information.box_converter import BoxConverter

class TextExtractor:
    def __init__(self, tesseract_cmd):
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def extract_text(self, image_path, box):
        """
        Extract text from a specified box in the image.

        :param image_path: Path to the original image
        :param box: EasyOCR box format [top-left, top-right, bottom-right, bottom-left]
        :return: Extracted text
        """
        image = Image.open(image_path)
        pil_box = BoxConverter.convert_box_to_pil_box(box)
        cropped_image = image.crop(pil_box)
        text = pytesseract.image_to_string(cropped_image, lang='eng')
        return text
