import os
from extract_information.box_converter import BoxConverter
from extract_information.text_extractor import  TextExtractor
from extract_information.text_summarizer import TextSummarizer
from extract_information.image_processor import ImageProcessor
from extract_information.vlm_processor import VLMProcessor
from gtts import gTTS

class Processor:
    def __init__(self, tesseract_cmd):
        self.text_extractor = TextExtractor(tesseract_cmd)
        self.image_processor = ImageProcessor()
        self.text_summarizer = TextSummarizer()
        self.vlm_processor = VLMProcessor()
    def process_image(self, image_path, boxes,sumarize):
        """
        Process the image and extract text and summaries from each specified box.

        :param image_path: Path to the original image
        :param boxes: List of bounding boxes in (x, y, w, h) format
        :param sumarize approach
        :return: List of results containing box coordinates, extracted text, summaries, and paths to cropped images
        """
        results = []
        box_index = 1

        boxes = BoxConverter.convert_boxes(boxes)
        for box in boxes:
            audio_path = os.path.join('myapp/static/cropped_audios', f"{box_index}.mp3")
            summary_audio_path = os.path.join('myapp/static/cropped_audios_summary', f"{box_index}.mp3")
            description_audio_path = os.path.join('myapp/static/cropped_audios_description',f"{box_index}.mp3" )
            
            text = self.text_extractor.extract_text(image_path, box)
            summary = ""
            
            if text.strip() and len(text) > 10 and any(char.isalpha() for char in text):    
                gTTS(text=text).save(audio_path)
                summary = self.text_summarizer.summarize_text(text,sumarize)
                
                if not summary.strip():
                    summary = text

                if any(char.isalpha() for char in summary):
                    gTTS(text=summary).save(summary_audio_path)
                
            cropped_image_path = self.image_processor.crop_and_save(image_path, box, box_index)
            
            descriptive_text = self.vlm_processor.extract_vlm_info(cropped_image_path)
            
            if descriptive_text.strip(): 
                gTTS(text=descriptive_text).save(description_audio_path)
            
            results.append({
                "id": box_index,
                "box": [[int(point[0]), int(point[1])] for point in box],
                "text": text,
                "summary": summary,
                "description": descriptive_text,
                "path": os.path.normpath(cropped_image_path),
                "audio_path": os.path.normpath(audio_path),
                "summary_audio_path": os.path.normpath(summary_audio_path),
                "description_audio_path" : os.path.normpath(description_audio_path)
            })
            box_index += 1
        return results


