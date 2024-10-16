from collections import defaultdict

import networkx as nx
import random

from matplotlib import pyplot as plt

from Node import *

class Topology:
    def __init__(self, num_anchor_nodes, topology_size , range_threshold):
        self.graph = nx.Graph()
        self.anchor_nodes = {}
        self.mobile_nodes = None
        self.topology_size = topology_size
        self.range_threshold = range_threshold

        # Calculate grid spacing
        spacing = topology_size / (num_anchor_nodes ** 0.5 + 1)

        # Place anchor nodes in a grid
        for i in range(num_anchor_nodes):
            col = i % int(num_anchor_nodes ** 0.5)
            row = i // int(num_anchor_nodes ** 0.5)
            x = (col + 1) * spacing
            y = (row + 1) * spacing
            anchor_node = AnchorNode(i, x, y)
            self.anchor_nodes[i] = anchor_node
            self.graph.add_node(i, type=anchor_node.type, position=(x, y))

    def add_mobile_node(self, node_id, x, y):
        mobile_node = MobileNode(node_id, x, y)
        self.mobile_nodes = mobile_node
        self.graph.add_node(node_id, type=mobile_node.type, position=(x, y))
        return mobile_node

    def move_mobile_node(self, mobile_node, x, y):
        mobile_node.x = x
        mobile_node.y = y
        self.graph.nodes[mobile_node.id]['position'] = (x, y)

    def add_edges_within_range(self):
        # Clear all existing edges in the graph
        self.graph.remove_edges_from(list(self.graph.edges))
        for node_id in self.graph.nodes():
            for other_id in self.graph.nodes():
                if node_id != other_id:
                    x1, y1 = self.graph.nodes[node_id]['position']
                    x2, y2 = self.graph.nodes[other_id]['position']
                    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                    if distance <= self.range_threshold:
                        self.graph.add_edge(node_id, other_id)


    def visualize_topology(self):
        pos = {n: self.graph.nodes[n]['position'] for n in self.graph.nodes}
        node_colors = ['lightblue' if self.graph.nodes[n]['type'] == NodeType.ANCHOR else 'red' for n in self.graph.nodes]
        node_sizes = [1000 if self.graph.nodes[n]['type'] == NodeType.MOBILE else 500 for n in self.graph.nodes]
        fig, ax = plt.subplots()
        self.add_edges_within_range()
        nx.draw(self.graph, pos, with_labels=True, node_color=node_colors, node_size=node_sizes, font_size=10, ax=ax)
        plt.show()

    def get_mobile_node_id(self):
        for node_id in self.graph.nodes():
            if self.graph.nodes[node_id]['type'] == NodeType.MOBILE:
                return node_id
        return None

    def delete_anchor_node(self, anchor_node_id):
        # Check if the anchor node ID exists in the anchor nodes dictionary
        if anchor_node_id in self.anchor_nodes:
            # Remove the anchor node from the anchor nodes dictionary and the graph
            del self.anchor_nodes[anchor_node_id]
            self.graph.remove_node(anchor_node_id)
        else:
            print(f"Anchor node with ID {anchor_node_id} does not exist.")


    def add_anchor_node(self,new_id,  x, y):

        anchor_node = AnchorNode(new_id, x, y)
        self.anchor_nodes[new_id] = anchor_node
        self.graph.add_node(new_id, type=anchor_node.type, position=(x, y))
    def compute_hop_table(self):
        source_mobile_node_id = self.get_mobile_node_id()

        if source_mobile_node_id is not None:
            # Create a directed graph from the topology
            graph = nx.Graph(self.graph)
            hop_table = {}

            # Iterate through anchor nodes
            for anchor_node_id in self.graph.nodes():
                if anchor_node_id != source_mobile_node_id:  # Skip the mobile node itself
                    try:
                        shortest_distance = nx.shortest_path_length(graph, source_mobile_node_id, anchor_node_id)
                    except nx.NetworkXNoPath:
                        shortest_distance = float('inf')

                    hop_table[anchor_node_id] = shortest_distance

            return hop_table
