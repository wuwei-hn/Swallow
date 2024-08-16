from collections import defaultdict


def find_key_by_value(dictionary, value):
    for key, nested_list in dictionary.items():
        if value in nested_list:
            return key
    return None


def assign_tasks(network, classification):
    tasks = defaultdict(list)
    unprogrammables = []
    area_man_nodes = []
    devices = network.get_devices()
    for device in devices:
        print(device.name)
        if device.category == 'programmable':
            area_man_nodes.append(device.name)
        else:
            unprogrammables.append(device.name)
    graph = network.get_network()
    for area_man_node in area_man_nodes:
        tasks[area_man_node] = []
    for node in graph:
        key_by_value = find_key_by_value(classification, node)
        if key_by_value != None:
            if node not in tasks[key_by_value]:
                tasks[key_by_value].append(node)
        else:
            tasks[key_by_value].append(node)
        node_last = list(graph.nodes)
        if node == node_last[-1] if node_last else None:
            continue
        successors = list(graph.neighbors(node))
        if successors.__len__() != 1:
            successor = successors[1]
            successor_key = find_key_by_value(classification, successor)
            if key_by_value != successor_key:
                tasks[key_by_value].append(successor)
        else:
            if successors[0] in area_man_nodes:
                node_last = list(graph.nodes)
                if node != node_last[-1] if node_last else None:
                    tasks[key_by_value].append(successors[0])
    return tasks