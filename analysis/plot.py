import networkx as nx
import matplotlib.pyplot as plt
import numpy as np



def plot_graph(graph, vertices, edges, graph_title):
    G = nx.Graph()
    G.clear()
    for edge in edges:
        G.add_edge(edge.node1.id, edge.node2.id)

    # explicitly set positions
    pos = {}
    if isinstance(vertices[0], list):
        vertices = [element for sublist in vertices for element in sublist]


    for vertex in vertices:
        pos[vertex] = (graph.nodes[vertex].x, graph.nodes[vertex].y)

    color_map = ['red' if graph.nodes[node].substation_id == -1 else 'white' for node in G]

    options = {
        "font_size": 7,
        "node_size": 200,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 2,
        "width": 2,
    }
    nx.draw(G, pos, node_color=color_map, with_labels=True)
    # nx.draw_networkx(G, pos, **options)

    # Set margins for the axes so that nodes aren't clipped
    ax = plt.gca()
    ax.margins(0.05)
    # plt.axis("off")
    plt.savefig("analysis/plots/graph" + graph_title + ".png", format="PNG")
    plt.clf()




def plot_metadata(wiring, sink_distributions):
    pass


def analyze_metadata(wiring, sink_distributions):
    wire_length_changes = []
    sink_distribution_changes = []

    for i, wire_lengths in enumerate(wiring):
        idx_of_largest_substation = sink_distributions[i][0].index(max(sink_distributions[i][0]))
        wire_change = []
        distribution_change = []
        # percent change in wire length from regular multisource prims for the other 3 versions
        for j in range(1, len(wire_lengths)):
            wire_change.append((wire_lengths[j] - wire_lengths[0]) / wire_lengths[0])

        for j in range(1, len(sink_distributions[i])):
            distribution_change.append((sink_distributions[i][j][idx_of_largest_substation] - sink_distributions[i][0][idx_of_largest_substation]) / sink_distributions[i][0][idx_of_largest_substation])
        wire_length_changes.append(wire_change)
        sink_distribution_changes.append(distribution_change)

    wlc_nd = np.array(wire_length_changes).T
    sdc_nd = np.array(sink_distribution_changes).T

    mean_wlc_0 = sum(wlc_nd[0]) / len(wlc_nd[0])
    mean_wlc_1 = sum(wlc_nd[1]) / len(wlc_nd[1])
    mean_wlc_2 = sum(wlc_nd[2]) / len(wlc_nd[2])

    var_wlc_0 = sum((i - mean_wlc_0) ** 2 for i in wlc_nd[0]) / len(wlc_nd[0])
    var_wlc_1 = sum((i - mean_wlc_1) ** 2 for i in wlc_nd[1]) / len(wlc_nd[1])
    var_wlc_2 = sum((i - mean_wlc_2) ** 2 for i in wlc_nd[2]) / len(wlc_nd[2])

    print("Mean and variance in wire length change for v0: ", mean_wlc_0, var_wlc_0)
    print("Mean and variance in wire length change for v1: ", mean_wlc_1, var_wlc_1)
    print("Mean and variance in wire length change for v2: ", mean_wlc_2, var_wlc_2)


    mean_sdc_0 = sum(sdc_nd[0]) / len(sdc_nd[0])
    mean_sdc_1 = sum(sdc_nd[1]) / len(sdc_nd[1])
    mean_sdc_2 = sum(sdc_nd[2]) / len(sdc_nd[2])

    var_sdc_0 = sum((i - mean_sdc_0) ** 2 for i in sdc_nd[0]) / len(sdc_nd[0])
    var_sdc_1 = sum((i - mean_sdc_1) ** 2 for i in sdc_nd[1]) / len(sdc_nd[1])
    var_sdc_2 = sum((i - mean_sdc_2) ** 2 for i in sdc_nd[2]) / len(sdc_nd[2])

    print("Mean and variance of change in sink distribution in largest substation for v0: ", mean_sdc_0, var_sdc_0)
    print("Mean and variance of change in sink distribution in largest substation for v1: ", mean_sdc_1, var_sdc_1)
    print("Mean and variance of change in sink distribution in largest substation for v2: ", mean_sdc_2, var_sdc_2)


    return wire_length_changes, sink_distribution_changes
