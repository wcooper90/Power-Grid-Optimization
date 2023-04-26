def prims(graph):
    # pick arbitrary first vertex to start MST from
    vertices_connected = set([graph.nodes[0].id])
    edges = []

    while len(vertices_connected) != len(graph.nodes):
        shortest_connection = (None, float('inf'))
        for id in vertices_connected:
            for edge in graph.nodes[id].edges:
                # check that connection is not between nodes already in the MST
                if edge.node1.id not in vertices_connected or edge.node2.id not in vertices_connected:
                    if edge.weight < shortest_connection[1]:
                        shortest_connection = (edge, edge.weight)

        if shortest_connection[0].node1.id not in vertices_connected:
            vertices_connected.add(shortest_connection[0].node1.id)
        else:
            vertices_connected.add(shortest_connection[0].node2.id)

        edges.append(shortest_connection[0])

    return edges, vertices_connected
