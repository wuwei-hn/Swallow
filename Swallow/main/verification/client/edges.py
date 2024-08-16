class Edge:
    def __init__(self, first_node, second_node):
        self.first_node = first_node
        self.second_node = second_node
        self.edge = []
        self.set_edge()

    def set_edge(self):
        self.edge = [self.first_node, self.second_node]

    def get_edge(self):
        return self.edge
