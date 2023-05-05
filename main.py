from helpers import *
from config import CONFIGURATION
from analysis.plot import *
from algorithms.max_flow import *
from algorithms.minimum_spanning_tree import *
from tqdm import tqdm



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
        graph = generate_random_graph(num_nodes, multi_source=True)
        minimum_spanning_tree_edges, vertices, meta = multi_source_prims(graph)
        idx_of_largest_substation = meta[-1][0]
        proportion_of_largest_substation = meta[-1][1]
        minimum_spanning_tree_edges1, vertices1, meta1 = multi_source_prims_v1(graph, idx_of_largest_substation)
        minimum_spanning_tree_edges2, vertices2, meta2 = multi_source_prims_v2(graph, idx_of_largest_substation)
        minimum_spanning_tree_edges3, vertices3, meta3 = multi_source_prims_v3(graph, idx_of_largest_substation)

        wires = [meta[0], meta1[0], meta2[0], meta3[0]]
        s_distribution = [meta[1], meta1[1], meta2[1], meta3[1]]

        wiring.append(wires)
        sink_distributions.append(s_distribution)

        plot_graph(graph, vertices, minimum_spanning_tree_edges, str(iter) + "plain")
        plot_graph(graph, vertices1, minimum_spanning_tree_edges1, str(iter) + "v1")
        plot_graph(graph, vertices2, minimum_spanning_tree_edges2, str(iter) + "v2")
        plot_graph(graph, vertices3, minimum_spanning_tree_edges3, str(iter) + "v3")


    wire_length_changes, sink_distribution_changes = analyze_metadata(wiring, sink_distributions)

    # for w in wire_length_changes:
    #     print(w)
    # print("*"*80)
    # for sdc in sink_distribution_changes:
    #     print(sdc)
    # plot_metadata(wiring, sink_distributions)


stochastic_simulation(50, 75)
