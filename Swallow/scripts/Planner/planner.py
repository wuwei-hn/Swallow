import math
import queue

import networkx
import time
from Planner.trans import trans
import re

result_queue = queue.Queue()
index = 0

class Planner:
    # 无限大
    INF = math.inf

    def __init__(self):
        self.devices = set()
        self.node_num = {}
        # self.parser = parser
        self.graph = networkx.Graph()
        self.ingresses = []

    def read_topology_from_file(self, filename):
        with open(filename, mode="r") as f:
            line = f.readline()
            while line:
                token = line.strip().split(" ")
                self.graph.add_node(token[0])
                self.graph.add_node(token[2])
                self.graph.add_edge(token[0], token[2])
                line = f.readline()

    def find_paths_of_length_n(self, start, end, length):
        def dfs(current, end, path, length):
            if length < 0:
                return
            if current == end or length == 0:
                paths.append(path)
                return
            for neighbor in self.graph.neighbors(current):
                if neighbor not in path:  # Avoid cycles
                    dfs(neighbor, end, path + [neighbor], length - 1)

        paths = []
        dfs(start, end, [start], length)
        return paths

    def find_all_path(self, start, end, path_exp):
        all_paths = self.find_paths_of_length_n(start, end, 12)
        # 编译正则表达式
        pattern = re.compile(path_exp)
        # 过滤出符合正则表达式的路径
        matching_paths = []
        for path in all_paths:
            path_str = ""
            index = 1
            for strs in path:
                if len(strs) == 1:
                    path_str = path_str + strs
                else:
                    if index != 1 and index != len(path):
                        strs = "S"
                        path_str = path_str + strs
                    else:
                        path_str = path_str + strs
                index = index + 1
            if pattern.match(path_str):
                matching_paths.append(path)
        # print(matching_paths.__len__())
        return matching_paths

    def gen(self, packet_add, dst, ingresses, behavior_raw, fault_scenes=None):

        global index
        behavior = trans(behavior_raw)
        file_path = '../dataset/Airtel1-2/preparation'

        if behavior is None:
            print("error in parse behavior!")
            return None

        self.ingresses = ingresses


        path_sum = behavior["path"]["path_exp"]
        path_exps = path_sum.split("|")
        k_dict = {
            "any_one": 1,
            "any_two": 2,
            "any_three": 3,
            None: 0,
        }
        k = 0 if fault_scenes not in k_dict else k_dict[fault_scenes]
        path_num = behavior["match"].split(" ")

        global result_queue

        for path_exp in path_exps:
            # print(path_exp)
            for ingress1 in ingresses:
                write_data = ""
                all_paths = self.find_all_path(ingress1, dst, path_exp)
                write_data = write_data + "preparation" + str(index) + "\n"
                write_data = write_data + "address:" + packet_add + "\n"
                write_data = write_data + "dst:" + dst + "\n" + "ingress:" +ingress1 + "\n"
                write_data = write_data + "match:" +behavior["match"] + "\n" + "path_exp:" + path_exp + "\n"
                write_data = write_data + "all_paths:" + "\n"
                for path in all_paths:
                    write_path = ",".join(path)
                    write_data = write_data + write_path + "\n"
                with open(file_path, 'a') as file:
                    file.write(write_data + "\n")
                index = index + 1
    def gen_all_pairs_reachability(self):

        global result_queue
        sums = 0
        start_time = time.time()
        for node1 in self.graph.nodes:
            for node2 in self.graph.nodes:
                if node1 == node2:
                    continue
                result_queue = self.gen(
                    "335544320 ", node1, [node2], r"(exist >= 1, (%s.*%s))" % (node2, node1),
                    fault_scenes=None
                )
                sums = sums + 1

        print(sums)
        return result_queue
