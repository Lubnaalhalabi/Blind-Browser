class BoxConverter:
    @staticmethod
    def convert_box_to_pil_box(box):
        """
        Convert EasyOCR box format to PIL box format.

        :param easyocr_box: List of four points [top-left, top-right, bottom-right, bottom-left]
        :return: Tuple (left, upper, right, lower) representing the PIL box format
        """
        left = min(point[0] for point in box)
        upper = min(point[1] for point in box)
        right = max(point[0] for point in box)
        lower = max(point[1] for point in box)
        return (left, upper, right, lower)

    @staticmethod
    def convert_boxes(box):
        """
        Convert bounding box format from (x, y, w, h) to EasyOCR's format.

        :param boxes: List of bounding boxes in (x, y, w, h) format
        :return: List of converted boxes in EasyOCR format [top-left, top-right, bottom-right, bottom-left]
        """
        x, y, w, h = box
        top_left = [x, y]
        top_right = [x + w, y]
        bottom_right = [x + w, y + h]
        bottom_left = [x, y + h]
        return  [[top_left, top_right, bottom_right, bottom_left]]

