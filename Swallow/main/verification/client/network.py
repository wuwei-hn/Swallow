import networkx as nx
from devices import Device
from edges import Edge


class Network:
    def __init__(self, XYNet, file_path):
        self.XYNet = XYNet
        self.network = nx.Graph()
        self.devices = []
        self.edges = []
        self.file_path = file_path
        self.add_edges()
        self.add_devices()
        self.set_devices_category()
        self.set_device_fw()
        # self.get_devices()

    def add_devices(self):
        for device in self.XYNet:
            self.network.add_node(device)
            if device == self.XYNet[len(self.XYNet) - 1]:
                continue
            self.devices.append(Device(device))

    def add_edges(self):
        for device1, device2 in zip(self.XYNet[:-1], self.XYNet[1:]):
            self.network.add_edge(device1, device2, capacity=1)
            self.edges.append(Edge(device1, device2))

    def get_network(self):
        return self.network

    def set_devices_category(self):
        device_path = self.file_path + "/devices_class"
        with open(device_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        # 处理每一行
        for line in lines:
            # 去除行尾的换行符，并按空格分割
            device, category = line.strip().split()
            index = 0
            for device1 in self.devices:
                if device1.name == device:
                    break
                index = index + 1
            if index == self.devices.__len__():
                continue
            else:
                self.devices[index].set_category(category)

    def set_device_fw(self):
        for device in self.devices:
            device.set_fw(self.file_path)

    def get_devices(self):
        return self.devices
