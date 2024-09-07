from preprocessing_datasets.data_processor import DataProcessor
from preprocessing_datasets.data_segmenter import DataSegmenter
from preprocessing_datasets.right_data_extractor import RightDataExtractor
from preprocessing_datasets.segment_comparator import SegmentComparator
import json

def main():

    # Initialize paths for processing the comparator results
    popular_dataset_path = "resources/mapping-popular.csv"
    random_dataset_path = "resources/mapping-random.csv"
    final_result = []


    # Process the popular dataset to create actual JSON data
    popular_data_processor = DataProcessor(popular_dataset_path, "resources/json-dataset-popular/actual")
    popular_data_processor.process()

    # Process the random dataset to create actual JSON data
    random_data_processor = DataProcessor(random_dataset_path, "resources/json-dataset-random/actual")
    random_data_processor.process()

    # Extract the right blocks from the actual popular dataset JSON files
    input_folder = 'resources/json-dataset-popular/actual'
    output_folder = 'resources/json-dataset-popular/actual_without_big_block'
    extractor_popular = RightDataExtractor(input_folder, output_folder)
    extractor_popular.process_all_files()

    # Extract the right blocks from the actual random dataset JSON files
    input_folder = 'resources/json-dataset-random/actual'
    output_folder = 'resources/json-dataset-random/actual_without_big_block'
    extractor_random = RightDataExtractor(input_folder, output_folder)
    extractor_random.process_all_files()

    # Segment the popular dataset to create predicted JSON data
    popular_data_segmenter = DataSegmenter(popular_dataset_path, "resources/json-dataset-popular/predicted")
    popular_data_segmenter.segment()

    # Segment the random dataset to create predicted JSON data
    random_data_segmenter = DataSegmenter(random_dataset_path, "resources/json-dataset-random/predicted")
    random_data_segmenter.segment()


    ##############################################################
    

    # Compare the segmented and actual data for the popular dataset
    comparator = SegmentComparator(popular_dataset_path, "resources/json-dataset-popular/predicted", "resources/json-dataset-popular/actual_without_big_block")
    results = comparator.process_all_domains()
    res1 = comparator.save_results(results, "results-popular.json")

    # Compare the segmented and actual data for the random dataset
    comparator = SegmentComparator(random_dataset_path, "resources/json-dataset-random/predicted", "resources/json-dataset-random/actual_without_big_block")
    results = comparator.process_all_domains()
    res2 = comparator.save_results(results, "results-random.json")

    # Append results to the final result list
    final_result.append(res1)
    final_result.append(res2)

    # Save the final overall metrics to a JSON file
    with open("final_results.json", "w") as file:
        json.dump(final_result, file, indent=4)

if __name__ == "__main__":
    main()
