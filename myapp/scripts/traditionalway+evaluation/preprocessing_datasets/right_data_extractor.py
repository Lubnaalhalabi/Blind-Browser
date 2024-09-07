import json
import os
import glob

class RightDataExtractor:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    @staticmethod
    def is_parent_or_ancestor(xpath1, xpath2):
        return xpath1.startswith(xpath2)

    def process_file(self, input_filepath, output_filepath):
        with open(input_filepath, 'r') as f:
            data = json.load(f)
        
        filtered_data = []
        for obj in data:
            xpath1 = obj["xPath"]
            should_keep = True
            for other_obj in data:
                if obj != other_obj:
                    xpath2 = other_obj["xPath"]
                    if self.is_parent_or_ancestor(xpath2, xpath1):
                        should_keep = False
                        break
            if should_keep:
                filtered_data.append(obj)
        
        with open(output_filepath, 'w') as f:
            json.dump(filtered_data, f, indent=4)

    def process_all_files(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        
        for input_filepath in glob.glob(os.path.join(self.input_folder, '*.json')):
            filename = os.path.basename(input_filepath)
            output_filepath = os.path.join(self.output_folder, filename)
            self.process_file(input_filepath, output_filepath)
