from domain_clusterer import DomainClusterer
import sys
def main(url):
    # Create an instance of DomainClusterer and perform clustering
    clusterer = DomainClusterer(url)
    clusterer.cluster_domains()
    res = clusterer.domain_clusters[0][1]
    return res

if __name__ == "__main__":
    url = sys.argv[1]
    result = main(url)
    print(result)
