from helpers import *
from config import CONFIGURATION
from analysis.plot import *
from algorithms.minimum_spanning_tree import *
from tqdm import tqdm
import numpy as np



# num_nodes = 4
#
# graph = generate_random_graph(num_nodes)
# graph = generate_random_graph(num_nodes, multi_source=True)
#
# minimum_spanning_tree_edges, vertices, wiring = prims(graph)
# print(wiring)
# minimum_spanning_tree_edges, vertices, metadata = multi_source_prims(graph)
# print(metadata)
#
#
# plot_graph(graph, vertices, minimum_spanning_tree_edges, "")


def stochastic_simulation(iterations, num_nodes):
    sink_distributions = []
    wiring = []
    for iter in tqdm(range(iterations)):
        graph = generate_random_graph(num_nodes, multi_source=True, fully_connected=False)

        # full_graph, random_graph = generate_random_and_fully_connected_graph(num_nodes)

        minimum_spanning_tree_edges, vertices, meta = multi_source_prims(graph)
        # minimum_spanning_tree_edges_full, vertices_full, meta_full = prims(full_graph)
        # minimum_spanning_tree_edges, vertices, meta = prims(random_graph)

        # wires = [meta[0], meta_full[0]]
        # wiring.append(wires)

        idx_of_largest_substation = meta[-1][0]
        proportion_of_largest_substation = meta[-1][1]
        # minimum_spanning_tree_edges1, vertices1, meta1 = multi_source_prims_v1(graph, idx_of_largest_substation)
        # minimum_spanning_tree_edges2, vertices2, meta2 = multi_source_prims_v2(graph, idx_of_largest_substation)
        # minimum_spanning_tree_edges3, vertices3, meta3 = multi_source_prims_v3(graph, idx_of_largest_substation)
        # minimum_spanning_tree_edges2, vertices2, meta2 = multi_source_prims_v2_change(graph, idx_of_largest_substation, change=0.02)
        # minimum_spanning_tree_edges3, vertices3, meta3 = multi_source_prims_v2_change(graph, idx_of_largest_substation, change=0.05)
        minimum_spanning_tree_edges4, vertices4, meta4 = multi_source_prims_v2_change(graph, idx_of_largest_substation, change=0.1)
        minimum_spanning_tree_edges5, vertices5, meta5 = multi_source_prims_v2_change(graph, idx_of_largest_substation, change=0.3)
        minimum_spanning_tree_edges6, vertices6, meta6 = multi_source_prims_v2_change(graph, idx_of_largest_substation, change=0.5)



        wires = [meta[0], meta4[0], meta5[0], meta6[0]]
        s_distribution = [meta[1], meta4[1], meta5[1], meta6[1]]

        wiring.append(wires)
        sink_distributions.append(s_distribution)

        # plot_graph(graph, vertices, minimum_spanning_tree_edges, str(iter) + "plain")
        # print([np.arange(0, 10)])
        # plot_graph(graph, [list(np.arange(0, 10, dtype=int))], graph.edges, 'full')
        # plot_graph(graph, vertices1, minimum_spanning_tree_edges1, str(iter) + "v1")
        # plot_graph(graph, vertices2, minimum_spanning_tree_edges2, str(iter) + "v2")
        # plot_graph(graph, vertices3, minimum_spanning_tree_edges3, str(iter) + "v3")


    wire_length_changes, sink_distribution_changes = analyze_metadata(wiring, sink_distributions)
    # return wiring


stochastic_simulation(100, 75)

# wiring = np.array(stochastic_simulation(100, 50)).T
# random_wires = wiring[0]
# full_wires = wiring[1]
#
# random_wires_avg = sum(random_wires) / len(random_wires)
# full_wires_avg = sum(full_wires) / len(full_wires)
# print(random_wires_avg, full_wires_avg)
