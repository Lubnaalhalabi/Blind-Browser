import json,csv
class SegmentComparator:
    def __init__(self, csv_file_path, predicted_segments_folder, actual_segments_folder):
        self.csv_file_path = csv_file_path
        self.predicted_segments_folder = predicted_segments_folder
        self.actual_segments_folder = actual_segments_folder
        # Initialize totals for overall metrics
        self.T_TP = 0
        self.T_FP = 0
        self.T_FN = 0
        self.T_TN = 0
        self.T_TS = 0

    def load_segments(self, folder, domain):
        """Load JSON segments for a given domain from the specified folder."""
        with open(f"{folder}/{domain}.json", "r") as file:
            return json.load(file)

    def compare_segments(self, segment1, segment2):
        # actual ==> seg2
        """Compare two segments to determine if they match based on xPath or cleaned text."""
        return (segment1['xPath'] == segment2['xPath']
                or
               segment1['text'].strip().replace('\n', '').strip() == segment2['text'].strip().replace('\n', '').strip()
                or 
               (
                segment2['x']*(1-0.08) <=segment1['x']<= segment2['x']*(1+0.08)
                and
                segment2['y']*(1-0.08) <=segment1['y']<= segment2['y']*(1+0.08)
                and 
                segment2['height']*(1-0.08) <=segment1['height']<= segment2['height']*(1+0.08)
                and
                segment2['width']*(1-0.08) <=segment1['width']<= segment2['width']*(1+0.08)
                )
               )
    def compute_metrics(self, segments1, segments2):
        """Compute TP, FP, FN, TN, and other metrics for two sets of segments."""
        TP = 0
        FP = 0
        FN = 0
        matched_indices = []

        # Iterate over segments1 to find matching segments in segments2
        for seg1 in segments1:
            matched = False
            for i, seg2 in enumerate(segments2):
                if self.compare_segments(seg1, seg2):
                    TP += 1
                    matched = True
                    matched_indices.append(i)
                    break
            if not matched:
                FP += 1

        # Count FN as segments in segments2 that were not matched
        FN = len([i for i in range(len(segments2)) if i not in matched_indices])

        # Calculate total segments and TN
        total_segments = len(segments1) + len(segments2) - TP
        TN = total_segments - TP - FP - FN

        # Update totals for overall metrics
        self.T_TP += TP
        self.T_FP += FP
        self.T_FN += FN
        self.T_TN += TN
        self.T_TS += total_segments

        # Calculate Precision, Recall, and F1Score
        Precision = TP / (TP + FP) if TP + FP != 0 else 0
        Recall = TP / (TP + FN) if TP + FN != 0 else 0
        F1Score = 2 * Precision * Recall / (Recall + Precision) if Recall + Precision != 0 else 0

        return {
            "Total Segments": total_segments,
            "True Positives (TP)": TP,
            "False Positives (FP)": FP,
            "False Negatives (FN)": FN,
            "True Negatives (TN)": TN,
            "Precision": Precision,
            "Recall": Recall,
            "F1Score": F1Score
        }

    def process_domain(self, domain):
        """Process a single domain to compute metrics."""
        predicted_segments = self.load_segments(self.predicted_segments_folder, domain)
        actual_segments = self.load_segments(self.actual_segments_folder, domain)
        return self.compute_metrics(predicted_segments, actual_segments)

    def process_all_domains(self):
        """Process all domains listed in the CSV file."""
        results = []
        with open(self.csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                domain = row["domain"]
                metrics = self.process_domain(domain)
                metrics["Domain"] = domain
                results.append(metrics)
        return results

    def save_results(self, results, file_path):
        """Save the results to a JSON file and print overall metrics."""
        with open(file_path, "w") as file:
            json.dump(results, file, indent=4)

        # Calculate final overall metrics
        Final_Precision = self.T_TP / (self.T_TP + self.T_FP) if self.T_TP + self.T_FP != 0 else 0
        Final_Recall = self.T_TP / (self.T_TP + self.T_FN) if self.T_TP + self.T_FN != 0 else 0
        Final_F1Score = 2 * Final_Precision * Final_Recall / (Final_Recall + Final_Precision) if Final_Recall + Final_Precision != 0 else 0

        return {
        "Dataset"    :file_path,
        "Total blocks": self.T_TS,
        "Correct blocks": self.T_TP,
        "Final Precision": Final_Precision,
        "Final Recall": Final_Recall,
        "Final F1Score": Final_F1Score
        }
