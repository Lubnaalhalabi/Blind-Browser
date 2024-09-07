from text_processor import TextProcessor
from url_content_extractor import URLContentExtractor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Class to cluster domains
class DomainClusterer:
    def __init__(self, url):
        self.url = url
        self.domain_clusters = []

    def cluster_domains(self):
        extractor = URLContentExtractor()
        processor = TextProcessor()

        domain = self.url.split('//')[1].split('/')[0]  # Extract domain name
        texts = extractor.extract_text(self.url)
        texts = [processor.preprocess_text(text) for text in texts if text]

        # Convert text data to numerical features
        if len(texts) < 2:
            print(f"Skipping {domain} due to insufficient text data.")

        vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2), min_df=1)
        try:
            data = vectorizer.fit_transform(texts)
        except ValueError as e:
            print(f"Skipping {domain} due to error: {e}")

        # Find the optimal number of clusters
        silhouette_scores = []
        max_clusters = min(200, data.shape[0] - 1)  # Ensure max_clusters is less than the number of samples
        cluster_range = range(2, max_clusters + 1)

        for n_clusters in cluster_range:
            if data.shape[0] >= n_clusters:  # Ensure there are enough samples for the number of clusters
                model = KMeans(n_clusters=n_clusters, random_state=42)
                cluster_labels = model.fit_predict(data)
                try:
                    silhouette_avg = silhouette_score(data, cluster_labels)
                    silhouette_scores.append(silhouette_avg)
                except ValueError as e:
                    silhouette_scores.append(float('-inf'))  # Append a very low score if an error occurs
            else:
                silhouette_scores.append(float('-inf'))  # Append a very low score if n_clusters > n_samples

        if not silhouette_scores:
            print(f"No valid silhouette scores computed for {domain}.")
            self.domain_clusters.append((domain, 0))  # Set default value 0 for clustering
            return
        
        optimal_cluster_index = silhouette_scores.index(max(silhouette_scores))
        optimal_num_clusters = cluster_range[optimal_cluster_index]

        # Store the optimal number of clusters for the domain
        self.domain_clusters.append((domain, optimal_num_clusters))
