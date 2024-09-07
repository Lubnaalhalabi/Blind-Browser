import os
from extract_information_tr.box_converter import BoxConverter
from extract_information_tr.text_summarizer import TextSummarizer
from extract_information_tr.image_processor import ImageProcessor
from extract_information_tr.vlm_processor import VLMProcessor
from gtts import gTTS

class Processor:
    def __init__(self):
        """
        Initializes the Processor with instances of ImageProcessor, TextSummarizer, 
        and VLMProcessor.
        """
        self.image_processor = ImageProcessor()
        self.text_summarizer = TextSummarizer()
        self.vlm_processor = VLMProcessor()
    def process_image(self, image, data ,sumarize):
        """
        Processes an image and associated data to extract and convert text to audio,
        summarize the text, and generate descriptive audio from cropped image sections.
        
        Parameters:
            image (PIL.Image.Image): The image to be processed.
            data (list of dict): A list of dictionaries where each dictionary contains
                                 information about the text and bounding box coordinates.
            sumarization approach
        
        Returns:
            list of dict: A list of dictionaries with the following keys:
                - "id" (int): The index of the record in the data list.
                - "box" (list of list of int): The coordinates of the bounding box after conversion.
                - "text" (str): The original text from the record.
                - "summary" (str): The summarized text.
                - "description" (str): The descriptive text extracted from the cropped image.
                - "path" (str): The file path to the cropped image.
                - "audio_path" (str): The file path to the audio generated from the original text.
                - "summary_audio_path" (str): The file path to the audio generated from the summary.
                - "description_audio_path" (str): The file path to the audio generated from the description.
        """
        results = []
        # Iterate over each record in the data
        for i, record in enumerate(data):
            # Extract text from the record
            text = record.get("text", "")
            # Define file paths for audio files
            audio_path = f"myapp\static\cropped_audios_tr\{i}.mp3"
            summary_audio_path = f"myapp\static\cropped_audios_summary_tr\{i}.mp3"
            description_audio_path = os.path.join('myapp/static/cropped_audios_description_tr',f"{i}.mp3" )

            summary = ""
            # Check if text is non-empty and has more than 10 characters with alphabetic characters
            if text.strip() and len(text) > 10 and any(c.isalpha() for c in text):
                # Convert text to speech and save it to the specified path
                gTTS(text=text).save(audio_path)
                
                # Summarize the text
                summary = self.text_summarizer.summarize_text(text,sumarize)
                
                # If summary is empty, use the original text
                if not summary.strip():
                    summary = text

                # Convert summary to speech and save it to the specified path
                if any(char.isalpha() for char in summary):
                    gTTS(text=summary).save(summary_audio_path)
            
            # Define the bounding box for cropping the image
            box = [
                int(round(record.get("x", 0))) + 200,
                int(round(record.get("y", 0))),
                int(round(record.get("width", 0))),
                int(round(record.get("height", 0)))
            ]
            # Convert the box coordinates
            box = BoxConverter.convert_boxes(box)

            # Crop the image based on the box coordinates and save it            
            cropped_image_path = self.image_processor.crop_and_save(image, box[0], i)
            
            # Extract descriptive text using the VLM processor            
            descriptive_text = self.vlm_processor.extract_vlm_info(cropped_image_path)
            
            # Convert descriptive text to speech and save it if the text is not empty            
            if descriptive_text.strip(): 
                gTTS(text=descriptive_text).save(description_audio_path)     

            # Append the results for the current record
            results.append({
                "id": i,
                "box": [[int(point[0]), int(point[1])] for point in box[0]],
                "text": text,
                "summary": summary,
                "description": descriptive_text,
                "path": os.path.normpath(cropped_image_path),
                "audio_path": os.path.normpath(audio_path),
                "summary_audio_path": os.path.normpath(summary_audio_path),
                "description_audio_path" : os.path.normpath(description_audio_path)
            })
        return results


