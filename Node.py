import networkx as nx
import random

class NodeType:
    MOBILE = 1
    ANCHOR = 2

class Node:
    def __init__(self, node_id, x, y):
        self.id = node_id
        self.x = x
        self.y = y

class AnchorNode(Node):
    def __init__(self, node_id, x, y):
        super().__init__(node_id, x, y)
        self.type = NodeType.ANCHOR

class MobileNode(Node):
    def __init__(self, node_id, x, y):
        super().__init__(node_id, x, y)
        self.type = NodeType.MOBILE
