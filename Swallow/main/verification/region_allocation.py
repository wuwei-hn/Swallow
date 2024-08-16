from collections import deque, defaultdict


def find_nearest_programmable_node(graph, start_node, uppercase_nodes):
    visited = set()
    queue = deque([(start_node, 0)])
    while queue:
        current_node, dist = queue.popleft()
        if current_node in visited:
            continue
        visited.add(current_node)
        if current_node in uppercase_nodes:
            return current_node
        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited:
                queue.append((neighbor, dist + 1))
    return None


def classify_nodes(network):
    unprogrammables = []
    programmables = []

    # 处理每一行
    devices = network.get_devices()
    for device in devices:
        if device.category == 'programmable':
            programmables.append(device.name)
        else:
            unprogrammables.append(device.name)
    graph = network.get_network()
    classification = defaultdict(list)
    for programmable in programmables:
        classification[programmable] = [programmable]
    for unprogrammable in unprogrammables:
        nearest_uppercase_node = find_nearest_programmable_node(graph, unprogrammable, programmables)
        if nearest_uppercase_node:
            classification[nearest_uppercase_node].append(unprogrammable)

    return classification