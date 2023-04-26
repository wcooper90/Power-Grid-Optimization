from helpers import *
from config import CONFIGURATION
from analysis.plot import *
from algorithms.max_flow import *
from algorithms.minimum_spanning_tree import *



num_nodes = 10

graph = generate_random_graph(num_nodes)

minimum_spanning_tree_edges, vertices = prims(graph)

# for edge in minimum_spanning_tree_edges:
#     print(edge.weight)
#
# print("*"*80)
# for edge in graph.edges:
#     print(edge.weight)
# print(vertices)

plot(graph, vertices, minimum_spanning_tree_edges)
