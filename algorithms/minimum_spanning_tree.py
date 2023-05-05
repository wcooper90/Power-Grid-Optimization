import sys
from pathlib import Path
import os
# set path to parent directory to be able to import instruction functions
sys.path.append(Path().parent)
from objects.NodeTypeEnum import NodeType
import math


def prims(graph):
    # pick arbitrary first vertex to start MST from
    vertices_connected = set([graph.nodes[0].id])
    edges = []
    metadata = []
    total_wiring = 0

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
        total_wiring += shortest_connection[1]

    return edges, vertices_connected, [total_wiring]


def multi_source_prims(graph):
    vertices_connected_set = []
    metadata = []
    total_wiring = 0
    num_substations = 0
    # initialize a set for each of the substations
    for node in graph.nodes:
        if node.type == NodeType.SUBSTATION:
            vertices_connected_set.append([node.id])
            num_substations += 1
    edges = []
    # since the substations don't need to be connected to each other,
    # count each of them in the covered set already
    num_connected_nodes = len(vertices_connected_set)

    while num_connected_nodes != len(graph.nodes):
        flat_set = [element for sublist in vertices_connected_set for element in sublist]
        shortest_connection = (None, float('inf'), None)
        for j, source_set in enumerate(vertices_connected_set):
            for id in source_set:
                for edge in graph.nodes[id].edges:
                    # check that connection is not between nodes already in the MST
                    if edge.node1.id not in flat_set or edge.node2.id not in flat_set:
                        if edge.weight < shortest_connection[1]:
                            shortest_connection = (edge, edge.weight, j)

        if shortest_connection[0].node1.id not in flat_set:
            vertices_connected_set[shortest_connection[2]].append(shortest_connection[0].node1.id)
            shortest_connection[0].node1.substation_id = shortest_connection[2]
        else:
            vertices_connected_set[shortest_connection[2]].append(shortest_connection[0].node2.id)
            shortest_connection[0].node2.substation_id = shortest_connection[2]

        edges.append(shortest_connection[0])
        total_wiring += shortest_connection[1]
        num_connected_nodes +=1

    sink_distribution = [len(sinks) for sinks in vertices_connected_set]
    metadata.append(total_wiring)
    metadata.append(sink_distribution)
    idx_of_largest_substation = None
    length_of_most_sinks = 0
    for i, sd in enumerate(sink_distribution):
        if sd > length_of_most_sinks:
            length_of_most_sinks = sd
            idx_of_largest_substation = i

    # append the index of the largest substation, and its proportion of the total sinks
    metadata.append((idx_of_largest_substation, idx_of_largest_substation/(num_connected_nodes - num_substations)))

    return edges, vertices_connected_set, metadata


def multi_source_prims_v1(graph, idx_of_largest_substation):
    vertices_connected_set = []
    metadata = []
    total_wiring = 0

    # initialize a set for each of the substations
    for node in graph.nodes:
        if node.type == NodeType.SUBSTATION:
            vertices_connected_set.append([node.id])
    edges = []
    # since the substations don't need to be connected to each other,
    # count each of them in the covered set already
    num_connected_nodes = len(vertices_connected_set)

    while num_connected_nodes != len(graph.nodes):
        flat_set = [element for sublist in vertices_connected_set for element in sublist]
        shortest_connection = (None, float('inf'), None)
        for j, source_set in enumerate(vertices_connected_set):
            multiplier = 1
            # if this is the source set for the largest substation, set its multiplier to something greater than 1
            # v1 is a constant multiplier
            if j == idx_of_largest_substation:
                multiplier = 1.1

            for id in source_set:
                for edge in graph.nodes[id].edges:
                    # check that connection is not between nodes already in the MST
                    if edge.node1.id not in flat_set or edge.node2.id not in flat_set:
                        if edge.weight * multiplier < shortest_connection[1]:
                            shortest_connection = (edge, edge.weight, j)

        if shortest_connection[0].node1.id not in flat_set:
            vertices_connected_set[shortest_connection[2]].append(shortest_connection[0].node1.id)
            shortest_connection[0].node1.substation_id = shortest_connection[2]
        else:
            vertices_connected_set[shortest_connection[2]].append(shortest_connection[0].node2.id)
            shortest_connection[0].node2.substation_id = shortest_connection[2]

        edges.append(shortest_connection[0])
        total_wiring += shortest_connection[1]
        num_connected_nodes +=1

    sink_distribution = [len(sinks) for sinks in vertices_connected_set]
    metadata.append(total_wiring)
    metadata.append(sink_distribution)

    return edges, vertices_connected_set, metadata


def multi_source_prims_v2(graph, idx_of_largest_substation):
    vertices_connected_set = []
    metadata = []
    total_wiring = 0

    # initialize a set for each of the substations
    for node in graph.nodes:
        if node.type == NodeType.SUBSTATION:
            vertices_connected_set.append([node.id])
    edges = []
    # since the substations don't need to be connected to each other,
    # count each of them in the covered set already
    num_connected_nodes = len(vertices_connected_set)


    distances = distance_between_substations(graph, idx_of_largest_substation)
    mult = 1 + 0.05 * (max(7 - distances[0], 0)) + 0.05 * (max(7 - distances[1], 0))

    while num_connected_nodes != len(graph.nodes):
        flat_set = [element for sublist in vertices_connected_set for element in sublist]
        shortest_connection = (None, float('inf'), None)
        for j, source_set in enumerate(vertices_connected_set):
            multiplier = 1
            # if this is the source set for the largest substation, set its multiplier to something greater than 1
            # v2 is based on the distance between substations
            if j == idx_of_largest_substation:
                multiplier = mult

            for id in source_set:
                for edge in graph.nodes[id].edges:
                    # check that connection is not between nodes already in the MST
                    if edge.node1.id not in flat_set or edge.node2.id not in flat_set:
                        if edge.weight * multiplier < shortest_connection[1]:
                            shortest_connection = (edge, edge.weight, j)

        if shortest_connection[0].node1.id not in flat_set:
            vertices_connected_set[shortest_connection[2]].append(shortest_connection[0].node1.id)
            shortest_connection[0].node1.substation_id = shortest_connection[2]
        else:
            vertices_connected_set[shortest_connection[2]].append(shortest_connection[0].node2.id)
            shortest_connection[0].node2.substation_id = shortest_connection[2]

        edges.append(shortest_connection[0])
        total_wiring += shortest_connection[1]
        num_connected_nodes +=1

    sink_distribution = [len(sinks) for sinks in vertices_connected_set]
    metadata.append(total_wiring)
    metadata.append(sink_distribution)

    return edges, vertices_connected_set, metadata


def multi_source_prims_v3(graph, idx_of_largest_substation):
    vertices_connected_set = []
    metadata = []
    total_wiring = 0

    # initialize a set for each of the substations
    for node in graph.nodes:
        if node.type == NodeType.SUBSTATION:
            vertices_connected_set.append([node.id])
    edges = []
    # since the substations don't need to be connected to each other,
    # count each of them in the covered set already
    num_connected_nodes = len(vertices_connected_set)

    while num_connected_nodes != len(graph.nodes):
        flat_set = [element for sublist in vertices_connected_set for element in sublist]
        shortest_connection = (None, float('inf'), None)
        for j, source_set in enumerate(vertices_connected_set):
            multiplier = 1
            # if this is the source set for the largest substation, set its multiplier to something greater than 1
            for id in source_set:
                for edge in graph.nodes[id].edges:
                    # check that connection is not between nodes already in the MST
                    if edge.node1.id not in flat_set or edge.node2.id not in flat_set:
                        # v1 multiplier is based on the distance between the current sink vertex and the substation
                        if j == idx_of_largest_substation:
                            d = None
                            if edge.node1.id not in flat_set:
                                d = dist_between_substation_and_vertex(graph, idx_of_largest_substation, edge.node1)
                            else:
                                d = dist_between_substation_and_vertex(graph, idx_of_largest_substation, edge.node2)
                            multiplier = 1 + 0.05 * (max(3 - d, 0))

                        if edge.weight * multiplier < shortest_connection[1]:
                            shortest_connection = (edge, edge.weight, j)

        if shortest_connection[0].node1.id not in flat_set:
            vertices_connected_set[shortest_connection[2]].append(shortest_connection[0].node1.id)
            shortest_connection[0].node1.substation_id = shortest_connection[2]
        else:
            vertices_connected_set[shortest_connection[2]].append(shortest_connection[0].node2.id)
            shortest_connection[0].node2.substation_id = shortest_connection[2]

        edges.append(shortest_connection[0])
        total_wiring += shortest_connection[1]
        num_connected_nodes +=1

    sink_distribution = [len(sinks) for sinks in vertices_connected_set]
    metadata.append(total_wiring)
    metadata.append(sink_distribution)

    return edges, vertices_connected_set, metadata


def distance_between_substations(graph, idx_of_largest_substation):
    substations = []
    distances = []
    for node in graph.nodes:
        if node.type == NodeType.SUBSTATION and node.id != idx_of_largest_substation:
            substations.append(node)

    distances.append(math.dist([substations[0].x, substations[0].y], [graph.nodes[idx_of_largest_substation].x, graph.nodes[idx_of_largest_substation].y]))
    distances.append(math.dist([substations[1].x, substations[1].y], [graph.nodes[idx_of_largest_substation].x, graph.nodes[idx_of_largest_substation].y]))
    return distances


def dist_between_substation_and_vertex(graph, idx_of_largest_substation, vertex):
    return math.dist([graph.nodes[idx_of_largest_substation].x, graph.nodes[idx_of_largest_substation].y], [vertex.x, vertex.y])
