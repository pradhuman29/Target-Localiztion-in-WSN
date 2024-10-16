import math

import networkx as nx
import random

import simpy
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from LocalizationAlgorithms import weighted_centroid
from Mobility_Model import MobilityModel
from Node import *
from Topology import Topology

# Assuming you have already defined your Topology and MobilityModel classes

# Create a topology
num_anchor_nodes = 50
topology_size = 200
range_threshold =  35
topology = Topology(num_anchor_nodes, topology_size, range_threshold)
droprate = 0

num_node_del = droprate*num_anchor_nodes//100
print(num_node_del)
# Add a mobile node to the topology
mobile_node = topology.add_mobile_node(num_anchor_nodes, 100, 100)

# Create a SimPy environment
env = simpy.Environment()

# Define speed and pause time ranges
speed_range = (20, 25)  # Example range, adjust as needed
 # Example range, adjust as needed
type =3
# Initialize a MobilityModel
#1 for random walk
#2 for ramdom waypoint
#3 for random direction

mobility_model = MobilityModel(topology, mobile_node, env, speed_range,topology_size*0.8 ,type )
RSME = []
# Set up the plot for animation
fig, ax = plt.subplots()
pos = {n: topology.graph.nodes[n]['position'] for n in topology.graph.nodes}
node_colors = ['lightblue' if topology.graph.nodes[n]['type'] == 'AnchorNode' else 'green' for n in topology.graph.nodes]
node_sizes = [1000 if topology.graph.nodes[n]['type'] == 'MobileNode' else 500 for n in topology.graph.nodes]
nx.draw(topology.graph, pos, with_labels=True, node_color=node_colors, node_size=node_sizes, font_size=10, ax=ax)
id_mobile  = topology.get_mobile_node_id()
error =[]
def update(frame):
    if frame > 0:
        env.run(until=frame)
        ax.clear()
        # Re-add edges within range
        random_integers = random.sample(range(0, num_anchor_nodes), num_node_del)
        delNode = []
        for i in random_integers:
            if i in topology.anchor_nodes :
                node = topology.anchor_nodes[i]
                delNode.append(node)
                topology.delete_anchor_node(i)
        # node =  topology.anchor_nodes[randNodeid]
        # topology.delete_anchor_node(randNodeid)
        topology.add_edges_within_range()

        for i in delNode :
            topology.add_anchor_node(i.id, i.x, i.y)
        pos = {n: topology.graph.nodes[n]['position'] for n in topology.graph.nodes}
        node_colors = ['lightblue' if topology.graph.nodes[n]['type'] ==  NodeType.ANCHOR else 'green' for n in topology.graph.nodes]
        node_sizes = [250 if topology.graph.nodes[n]['type'] == NodeType.MOBILE else 500 for n in topology.graph.nodes]
        nx.draw(topology.graph, pos, with_labels=True, node_color=node_colors, node_size=node_sizes, font_size=10, ax=ax)
        # Call visualize_topology to update the positions of mobile nodes in the visualization
        actualx, actualy = topology.mobile_nodes.x, topology.mobile_nodes.y
        hop = topology.compute_hop_table()
        # dropping a random node
        predictedx, predictedy = weighted_centroid(hop , topology)
        #weighted_centroid(hop, topology)
        print(f"actual : {actualx , actualy}")
        print(f"predicted : {predictedx , predictedy}")

        # Calculate MSE
        mse = (predictedx - actualx) ** 2 + (predictedy - actualy) ** 2
        error.append(mse)

        # Draw the actual and predicted locations
        plt.scatter(actualx, actualy, color='green', marker='o', s=100, label='Actual')
        plt.scatter(predictedx, predictedy, color='red', marker='x', s=100, label='Predicted')

        # Add legend
        plt.legend()

        # Adjust plot limits if needed
        plt.xlim(0, topology_size)
        plt.ylim(0, topology_size)

'''
        adjacency_matrix = nx.to_numpy_array(topology.graph)
        print("Adjacency Matrix:")
        print(adjacency_matrix)
'''

# Create an animation
ani = FuncAnimation(fig, update, frames=range(100), repeat=False, interval=1000) # Adjust interval as needed
plt.show()

rsme =  math.sqrt(sum(error)/len(error))
print('rsme = ' ,rsme)
