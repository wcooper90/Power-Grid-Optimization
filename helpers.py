from config import CONFIGURATION
from objects.SourceNode import SourceNode
from objects.SinkNode import SinkNode
from objects.NodeTypeEnum import NodeType
from objects.Node import Node
from objects.Edge import Edge
from objects.Graph import Graph
import random
import math
import copy


def generate_random_graph(num_nodes, multi_source=False, fully_connected=False):
    config = CONFIGURATION()
    nodes = generate_nodes(num_nodes)
    if multi_source:
        assign_nodes(nodes, config.num_substations)
    edges = generate_edges(nodes, fully_connected)
    graph = Graph(nodes, edges)
    return graph


def generate_random_and_fully_connected_graph(num_nodes):
    config = CONFIGURATION()
    nodes = generate_nodes(num_nodes)
    full_nodes = copy.deepcopy(nodes)
    edges = generate_edges(nodes, False)
    full_edges = generate_edges(full_nodes, True)
    random_graph = Graph(nodes, edges)
    full_graph = Graph(full_nodes, full_edges)
    return full_graph, random_graph


def generate_nodes(num_nodes):
    config = CONFIGURATION()
    nodes = []
    for i in range(num_nodes):
        x_coord = random.random() * config.x_max
        y_coord = random.random() * config.y_max
        edges = []
        nodes.append(Node(i, x_coord, y_coord, edges))
    return nodes


def assign_nodes(nodes, num_substations):
    num_nodes = len(nodes)
    # assign a number of random substation locations
    for i in range(num_substations):
        substation = random.randint(0, num_nodes - 1)
        nodes[substation].type = NodeType.SUBSTATION
    # assign the rest to be sinks
    for i in range(num_nodes):
        if nodes[i].type == None:
            nodes[i].type == NodeType.SINK



"""
be able to generate random edges (like an already existing power grid?), or start off with
a fully connected graph
"""
def generate_edges(nodes, fully_connected=False):
    config = CONFIGURATION()
    max_dist = math.dist([0, 0], [config.x_max, config.y_max])
    edges = []
    for node in nodes:
        for i in range(len(nodes)):
            if i != node.id:
                if fully_connected:
                    e = Edge(node, nodes[i], euclidean_distance(node, nodes[i]))
                    edges.append(e)
                    node.edges.append(e)
                    if config.undirected:
                        nodes[i].edges.append(e)

                    # fix this probability later
                elif random.random() > euclidean_distance(node, nodes[i]) / max_dist:
                    # the weight of the edge will just be the euclidean distance for now
                    e = Edge(node, nodes[i], euclidean_distance(node, nodes[i]))
                    edges.append(e)
                    node.edges.append(e)
                    if config.undirected:
                        nodes[i].edges.append(e)
    return edges


def euclidean_distance(node1, node2):
    return math.dist([node1.x, node1.y], [node2.x, node2.y])
