import json
class JSONSaver:
    @staticmethod
    def save_results_to_json(results, filename):
        """
        Save the results to a JSON file.

        :param results: List of results to save
        :param filename: Name of the JSON file
        """
        with open(filename, 'w') as json_file:
            json.dump(results, json_file, indent=4)