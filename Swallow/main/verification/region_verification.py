import time
import tracemalloc

from verification.device_fwd import Fwd


def verification(area, packet_space, result, wrong_node, graph, time_queue):
    tracemalloc.start()
    start_time = time.time()
    rmul = 1
    packet_space = int(packet_space)
    devices = graph.get_devices()
    for node1, node2 in zip(area[:-1], area[1:]):
        judge = "false"
        for device in devices:
            if device.name == node1:
                node_fwds = device.get_fw()
                for node_fwd in node_fwds:
                    address = int(node_fwd["address"][0])
                    prefix = int(node_fwd["prefix"][0])
                    packet_space = int(packet_space)
                    if packet_space < address or packet_space > (address + pow(2, (32-prefix))):
                        continue
                    if node2 in node_fwd["forward"]:
                        judge = "true"
                        fund = 1
                        rmul = rmul * fund
                        break
        if judge == "false":
            fund = 0
            rmul = rmul * fund
            wrong_node.put(node1)
            wrong_node.put(node2)
            break
    result.put(rmul)
    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000
    time_queue.put(elapsed_time)
    print(f"{area}:{elapsed_time}ms \n")
    current, peak = tracemalloc.get_traced_memory()
    memory = (peak - current) / (1024 * 1024)