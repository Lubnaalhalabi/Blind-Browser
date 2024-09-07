from preprocessing_darasets_sam_algo.data_processor import DataProcessor
from preprocessing_darasets_sam_algo.segment_comparator import SegmentComparator
import json

def main():

    # Initialize paths for processing the comparator results
    random_dataset_path = "resources/mapping-random-samAlgo.csv"
    final_result = []

    # Process the random dataset to create actual JSON data
    random_data_processor = DataProcessor(random_dataset_path, "resources/json-dataset-random/predict-sam")
    random_data_processor.process()

    # Compare the segmented and actual data for the random dataset
    comparator = SegmentComparator(random_dataset_path, "resources/json-dataset-random/predict-sam", "resources/json-dataset-random/actual_without_big_block")
    results = comparator.process_all_domains()
    res2 = comparator.save_results(results, "results-random-sam.json")

    # Append results to the final result list
    final_result.append(res2)

    # Save the final overall metrics to a JSON file
    with open("final_results_sam.json", "w") as file:
        json.dump(final_result, file, indent=4)

if __name__ == "__main__":
    main()
