import networkx as nx
import matplotlib.pyplot as plt



def plot(graph, vertices, edges):
    G = nx.Graph()
    for edge in edges:
        G.add_edge(edge.node1.id, edge.node2.id)

    # explicitly set positions
    pos = {}
    for vertex in vertices:
        pos[vertex] = (graph.nodes[vertex].x, graph.nodes[vertex].y)

    options = {
        "font_size": 36,
        "node_size": 3000,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 5,
        "width": 5,
    }
    nx.draw_networkx(G, pos, **options)

    # Set margins for the axes so that nodes aren't clipped
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    plt.savefig("Graph.png", format="PNG")
