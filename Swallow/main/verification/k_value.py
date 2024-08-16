import networkx as nx
class K_value:
    def __init__(self, file_path):
        self.network = nx.Graph()
        self.devices = []
        self.edges = []
        self.file_path = file_path
        self.read_topology()


    def get_network(self):
        return self.network

    def read_topology(self):
        topo_path = self.file_path + "/topology"
        with open(topo_path, 'r', encoding='utf-8') as file:
            lines = file.readline()
            while lines:
                token = lines.strip().split(" ")
                self.network.add_node(token[0])
                self.network.add_node(token[2])
                self.network.add_edge(token[0], token[2], capacity=1)
                lines = file.readline()

    def find_max_failure_edges(self):
        min_cut_value = float('inf')
        nodes = list(self.network.nodes)
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                cut_value, partition = nx.minimum_cut(self.network, nodes[i], nodes[j], capacity='capacity')
                if cut_value < min_cut_value:
                    min_cut_value = cut_value
        print(f"最大失败链路数为: {min_cut_value}")

