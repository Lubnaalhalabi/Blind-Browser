import math
from bs4 import BeautifulSoup

class Segmentation:
    def __init__(self, tagSpa,n_list_dom,soup):
        self.tagSpa = tagSpa
        self.soup = soup
        self.n_list_dom = n_list_dom
    # Find the largest nodes in the dictionary list
    def find_largest_nodes(self,elements):
        for i in range(0, len(elements)):
            # Check if node is non-empty and eligible for segmentation
            if (elements[i][i]['tagName'] != "" and elements[i][i]['seg'] != "false"):
                # Get the space value of the first eligible node
                large_node = float(elements[i][i]['space'])
                break
        large = []
        # Determine the largest node
        for i in range(0, len(elements)):
            if (elements[i][i]['tagName'] != "" and elements[i][i]['seg'] != "false"):
                if large_node <= float(elements[i][i]['space']):
                    large_node = float(elements[i][i]['space'])
        # Collect all nodes that have the largest space value
        for i in range(0, len(elements)):
            if (elements[i][i]['tagName'] != "" and elements[i][i]['seg'] != "false"):
                if large_node == float(elements[i][i]['space']):
                    large.append(i)
        return large
    
    # Find the smallest nodes in the dictionary list
    def find_smallest_nodes(self,elements):
        for i in range(0, len(elements)):
            # Check if node is non-empty
            if (elements[i][i]['tagName'] != ""):
                # Get the space value of the first non-empty node
                small_node = float(elements[i][i]['space'])
                break
        small = []
        # Determine the smallest node
        for i in range(0, len(elements)):
            if (elements[i][i]['tagName'] != ""):
                if small_node >= float(elements[i][i]['space']):
                    small_node = float(elements[i][i]['space'])
        # Collect all nodes that have the smallest space value
        for i in range(0, len(elements)):
            if (elements[i][i]['tagName'] != ""):
                if small_node == float(elements[i][i]['space']):
                    small.append(i)
        return small

    # Find the nearest nodes
    def find_nearest_nodes(self,elements ,index):
        mindistance = math.inf
        nearest_nodes = []
        for i in range(0, len(elements)):
            if (elements[i][i]['tagName'] != ""):
                # Skip the same node
                if (i == index):
                    continue
                else:
                    # Calculate the distance between nodes
                    distane = math.sqrt((float(self.tagSpa[i][i]['xCentre']) - float(self.tagSpa[index][index]['xCentre'])) ** 2 + (
                            float(self.tagSpa[i][i]['yCentre']) - float(self.tagSpa[index][index]['yCentre'])) ** 2)
                    if (distane < mindistance):
                        mindistance = distane
        # Collect all nodes that have the minimum distance
        for i in range(0, len(elements)):
            if (elements[i][i]['tagName'] != ""):
                distane = math.sqrt((float(self.tagSpa[i][i]['xCentre']) - float(self.tagSpa[index][index]['xCentre'])) ** 2 + (
                        float(self.tagSpa[i][i]['yCentre']) - float(self.tagSpa[index][index]['yCentre'])) ** 2)
                if mindistance == distane:
                    nearest_nodes.append(i)
        return nearest_nodes, mindistance

    # Reduce the number of clusters by merging nodes
    def reduce_clusters(self):
        smallest_nodes = self.find_smallest_nodes(self.tagSpa)
        min_node = smallest_nodes[0]
        nearest_nodes, _ = self.find_nearest_nodes(self.tagSpa, min_node)
        index_nearest = nearest_nodes[0]

        newtagSpa = []
        for i, element in enumerate(self.tagSpa):
            if i != min_node and i != index_nearest:
                newtagSpa.append(element)
            elif i == min_node:
                x = min(self.tagSpa[min_node][min_node]['x'], self.tagSpa[index_nearest][index_nearest]['x'])
                y = min(self.tagSpa[min_node][min_node]['y'], self.tagSpa[index_nearest][index_nearest]['y'])
                w = max(self.tagSpa[min_node][min_node]['x'] + self.tagSpa[min_node][min_node]['width'],
                        self.tagSpa[index_nearest][index_nearest]['x'] + self.tagSpa[index_nearest][index_nearest]['width'])
                h = max(self.tagSpa[min_node][min_node]['y'] + self.tagSpa[min_node][min_node]['height'],
                        self.tagSpa[index_nearest][index_nearest]['y'] + self.tagSpa[index_nearest][index_nearest]['height'])
                width = w - x
                height = h - y
                mixtagSpace = {
                    min_node: {
                        'tagName': self.tagSpa[min_node][min_node]['tagName'] + self.tagSpa[index_nearest][index_nearest]['tagName'],
                        'x': x,
                        'y': y,
                        'width': width,
                        'height': height,
                        'space': width * height,
                        'xCentre': width / 2 + x,
                        'yCentre': height / 2 + y,
                        'text': self.tagSpa[min_node][min_node]['text'] + self.tagSpa[index_nearest][index_nearest]['text'],
                        'seg': "false",
                        'xPath': self.tagSpa[min_node][min_node]['xPath'] + self.tagSpa[index_nearest][index_nearest]['xPath']
                    }
                }
                newtagSpa.append(mixtagSpace)
            else:
                newtagSpa.append({index_nearest: {'tagName': "", 'x': "", 'y': "", 'width': "", 'height': "", 'space': "", 'xCentre': "", 'yCentre': "", 'text': "", 'seg': "false", 'xPath': ""}})
        self.tagSpa = newtagSpa
        self.n_list_dom -= 1

    # Expand the number of clusters by splitting nodes 
    def expand_clusters(self):
        largest_nodes = self.find_largest_nodes(self.tagSpa)
        if not largest_nodes:
            return
        largechildren = largest_nodes[0]
        minchildren = math.inf
        for node in largest_nodes:
            nodepath = self.tagSpa[node][node]['xPath']
            directchildren = self.soup.find(attrs={'data-xpath': nodepath}).findChildren(recursive=False)
            if len(directchildren) < minchildren and directchildren:
                minchildren = len(directchildren)
                largechildren = node

        nodepath = self.tagSpa[largechildren][largechildren]['xPath']
        directchildren = self.soup.find(attrs={'data-xpath': nodepath}).findChildren(recursive=False)
        if not directchildren:
            self.tagSpa[largechildren][largechildren]['seg'] = 'false'
            return

        newtagSpa = []
        for i, element in enumerate(self.tagSpa):
            if i != largechildren:
                newtagSpa.append(element)
            else:
                newtagSpa.append({largechildren: {'tagName': "", 'x': "", 'y': "", 'width': "", 'height': "", 'space': "", 'xCentre': "", 'yCentre': "", 'text': "", 'seg': "false", 'xPath': ""}})

        self.tagSpa = newtagSpa
        self.n_list_dom += len(directchildren) - 1
        for ch in directchildren:
            if ch.get('data-cleaned') or not ch.get('data-bbox'):
                self.n_list_dom -= 1
                continue
            boundingVal = ch.get('data-bbox').split()
            self.tagSpa.append({
                len(self.tagSpa): {
                    'tagName': ch.name,
                    'x': float(boundingVal[0]),
                    'y': float(boundingVal[1]),
                    'width': float(boundingVal[2]),
                    'height': float(boundingVal[3]),
                    'space': float(boundingVal[4]),
                    'xCentre': float(boundingVal[0]) + float(boundingVal[2]) / 2,
                    'yCentre': float(boundingVal[1]) + float(boundingVal[3]) / 2,
                    'text': ch.text,
                    'seg': "true",
                    'xPath': ch.get('data-xpath')
                }
            })

    # Perform segmentation to cluster webpage elements
    def segmentation(self, n_zone, max_iter):
        self.n_zone = n_zone
        self.max_iter = max_iter
        n_iter = 1
        while n_iter < self.max_iter:
            if self.n_zone == self.n_list_dom:
                break
            elif self.n_zone < self.n_list_dom:
                self.reduce_clusters()
            else:
                self.expand_clusters()
            n_iter += 1
        return self.tagSpa
