import numpy as np
from sklearn.cluster import DBSCAN

# Class for clustering centroids
class Clustering:
    def perform_clustering(self, centroids, eps=10, min_samples=2):
        """
        Perform DBSCAN clustering on a set of centroids.

        Parameters:
        centroids (list): A list of centroid coordinates (x, y) to be clustered.
        eps (float): The maximum distance between two samples for them to be considered as in the same neighborhood. Default is 10.
        min_samples (int): The number of samples (or total weight) in a neighborhood for a point to be considered as a core point. Default is 2.

        Returns:
        tuple: A tuple containing:
            - labels (numpy.ndarray): The cluster labels for each point.
            - centers (numpy.ndarray): The coordinates of cluster centers, excluding noise points.
        """
        # Convert the list of centroids to a NumPy array
        centroids = np.array(centroids)

        # Perform DBSCAN clustering on the centroids
        db = DBSCAN(eps=eps, min_samples=min_samples).fit(centroids)

        # Extract the cluster labels assigned by DBSCAN
        labels = db.labels_

        # Get the unique cluster labels (excluding noise points labeled as -1)
        unique_labels = set(labels)

        # Calculate the centers of each cluster by averaging the coordinates of centroids in the same cluster
        centers = [centroids[labels == label].mean(axis=0) for label in unique_labels if label != -1]

        # Return the cluster labels and the coordinates of the cluster centers
        return labels, np.array(centers)