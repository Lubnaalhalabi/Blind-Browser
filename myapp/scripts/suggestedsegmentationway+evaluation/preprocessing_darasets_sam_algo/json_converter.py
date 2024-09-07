import json
import os
import logging

logging.basicConfig(level=logging.DEBUG)

# Convert clustered zones to JSON format
class JSONConverter:
    def __init__(self, zon, domain,saving_path):
        self.zon = zon
        self.domain = domain 
        self.saving_path = saving_path
    # Convert clustered zones to JSON format
    def convert_to_json(self):
        directory_json = []
        for node in range(0, len(self.zon)):
            if self.zon[node][node]['tagName'] != "":
                directory_json.append(self.zon[node][node])
        json_object = json.dumps(directory_json, indent=4)
        
        os.makedirs(os.path.dirname(self.saving_path), exist_ok=True)
        with open(self.saving_path, "w") as outfile:
            outfile.write(json_object)
        
        logging.info(f"JSON successfully saved to {self.saving_path}")

