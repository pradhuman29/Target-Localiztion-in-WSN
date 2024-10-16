import math

import numpy as np
from scipy.optimize import fsolve
from scipy.spatial import distance
from sklearn.manifold import MDS
def weighted_centroid(hop_table, topology):
    anchor_nodes = topology.anchor_nodes
    x_sum =0
    y_sum = 0
    total_weight =0
    for node in anchor_nodes :
        weight = 1/hop_table[node]**2
        x = anchor_nodes[node].x
        y = anchor_nodes[node].y
        total_weight += weight
        x_sum += weight*x
        y_sum += weight*y


    estimated_x = x_sum / total_weight
    estimated_y = y_sum / total_weight

    return estimated_x, estimated_y


def MDS_Localization(hop , topology) :
    anchor_nodes = topology.anchor_nodes
    mobile_nodes =  topology.mobile_nodes
    coordinates = []
    for node in anchor_nodes:
        coordinates.append([anchor_nodes[node].x , anchor_nodes[node].y])

    coordinates.append([mobile_nodes.x , mobile_nodes.y])
    dissimilarity_matrix = distance.squareform(distance.pdist(coordinates))

    # Apply MDS to obtain the map
    embedding = MDS(n_components=2, dissimilarity='precomputed')
    map_coords = embedding.fit_transform(dissimilarity_matrix)
    indexmobile  =  len(coordinates) -1
    n1=  map_coords[indexmobile -1]
    n2 =  map_coords[indexmobile -2]
    n3 = map_coords[indexmobile -3]
    target =  map_coords[indexmobile]

    d1 = math.sqrt((n1[0] - target[0])**2 + (n1[1] - target[1])**2)
    d2 = math.sqrt((n2[0] - target[0]) ** 2 + (n2[1] - target[1]) ** 2)
    d3 = math.sqrt((n3[0] - target[0]) ** 2 + (n3[1] - target[1]) ** 2)
    c1 = coordinates[indexmobile -1]
    c2 = coordinates[indexmobile -2]
    c3 = coordinates[indexmobile -3]

    def trilateration_eq(z):
        x = z[0]
        y = z[1]
        f1 = (x - c1[0]) ** 2 + (y - c1[1]) ** 2 - d1 ** 2
        f2 = (x - c2[0]) ** 2 + (y - c2[1]) ** 2 - d2 ** 2


        return np.array([f1 , f2])

    # Initial guess for the target coordinates
    x_guess = 1
    y_guess = 0

    # Solve the trilateration equations
    z0 = np.array([x_guess , y_guess])
    tval =  fsolve(trilateration_eq , z0)
    return tval;

