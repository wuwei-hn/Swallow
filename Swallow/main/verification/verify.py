import pickle
import socket
import threading
import time
import multiprocessing
from util.parse import Parse
from util.network import Network
import networkx as nx
import queue
# from py.main.util.parse import Parse
from verification.region_allocation import classify_nodes
from verification.task_assignment import assign_tasks

from verification.region_verification import verification
from client.client import Client

server_running = True
clients = {}
result_queue = queue.Queue()
wrong_node_queue = queue.Queue()
time_queue = queue.Queue()
stop = "False"


class Verify:
    def __init__(self, file_path):
        self.file_path = file_path
        self.address = ""
        self.dst = ""
        self.ingress = ""
        self.match = ""
        self.path_exp = ""
        self.all_paths = []
        self.sum_result = 1
        self.clear_path_file()
        self.result = []
        self.tasks = None

    def clear_path_file(self):
        with open("path", 'w') as file:
            pass  # 不需要写入任何内容，只需打开和关闭文件即可清空其内容

    def get_result(self):
        return self.result

    def handle_client(self, client_socket, client_address):
        global server_running
        while server_running:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                print(f"Received message from {client_address}: {data}")
                result = data.split(',')
                if len(result) > 2:
                    result_queue.put(int(result[0]))
                    wrong_node_queue.put(result[1])
                    wrong_node_queue.put(result[2])
                else:
                    if result[0] == '1':
                        result_queue.put(int(result[0]))
                    else:
                        device = result[0]
                        clients[device] = Client(client_address, client_socket)
                        if clients.__len__() == 3:
                            self.send_messages_to_clients()
            except ConnectionResetError:
                break
            if result_queue.qsize() == self.tasks.keys().__len__():
                self.stop_server()
                self.send_messages_to_clients()
                break

    def start_server(self, host, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen()
        global server_running
        server_running = True
        print(f"Server listening on {host}:{port}")
        thread = []
        i = 0
        try:
            while i < 3:
                client_socket, client_address = server_socket.accept()
                t = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                thread.append(t)
                t.start()
                i = i + 1
            for t in thread:
                t.join()
        finally:
            server_socket.close()

    def send_messages_to_clients(self):
        global server_running
        if not server_running:
            for area_man, area in self.tasks.items():
                if area_man is None:
                    continue
                client_add = clients[area_man].get_client_socket()
                client_add.sendall('quit'.encode())
            return
        for area_man, area in self.tasks.items():
            if area_man is None:
                continue
            message = ','.join(area)
            client_add = clients[area_man].get_client_socket()
            client_add.sendall(message.encode())

    def stop_server(self):
        global server_running
        server_running = False

    def get_tasks(self):
        return self.tasks

    def verify(self):
        file_parse = Parse(self.file_path + '\preparation')
        file_parse.set_preparation()
        preparations = file_parse.get_preparation()
        for preparation in preparations:
            self.address = preparation["address"]
            self.dst = preparation["dst"]
            self.ingress = preparation["ingress"]
            self.match = preparation["match"]
            self.path_exp = preparation["path_exp"]
            for path in preparation["all_paths"]:
                path = path.split(',')
                self.all_paths.append(path)

            while self.all_paths.__len__() != 0:
                start_time = time.time()

                shortest_path = min(self.all_paths, key=len)
                if shortest_path.__len__() == 0:
                    self.sum_result = 0
                    break
                print(shortest_path)
                self.sum_result = 1
                G = Network(shortest_path, self.file_path)
                classification = classify_nodes(G)
                self.tasks = assign_tasks(G, classification)
                for area_man, area in self.tasks.items():
                    print(f"{area_man}: {area}")
                threads = []
                global result_queue
                global wrong_node_queue
                global time_queue
                end_time = time.time()
                elapsed_time = (end_time - start_time) * 1000
                print(f"init:{elapsed_time}ms")
                for area_man, area in self.tasks.items():
                    if area_man is None:
                        verification(area, self.address, result_queue, wrong_node_queue, G, time_queue)
                    else:
                        self.start_server('0.0.0.0', 12345)
                        break
                start_time = time.time()
                max_value = 0

                results = []
                while not result_queue.empty():
                    results.append(result_queue.get())
                while not wrong_node_queue.empty():
                    # 打印所有结果
                    specific_edge = (wrong_node_queue.get(), wrong_node_queue.get())
                    self.all_paths = [path for path in self.all_paths if specific_edge not in zip(path[:-1], path[1:])]
                for result in results:
                    print(result)
                    self.sum_result = self.sum_result * result
                if self.sum_result == 1:
                    self.result.append(self.sum_result)
                    print("Verification successful")
                    end_time = time.time()
                    elapsed_time = (end_time - start_time) * 1000
                    max_value = max_value + elapsed_time
                    print(f"verification:{max_value}ms")
                    # 指定文件路径
                    file_path = 'path'
                    # 清空文件内容并写入新的内容
                    write_path = ",".join(shortest_path)
                    with open(file_path, 'a') as file:
                        file.write(write_path + "\n")
                    break
                else:
                    print("Verification failed")
            if self.sum_result == 0:
                self.result.append(self.sum_result)

    def non_redundant(self):
        path_num = 0
        file_parse = Parse(self.file_path + '\preparation')
        file_parse.set_preparation()
        preparations = file_parse.get_preparation()
        for preparation in preparations:
            self.address = preparation["address"]
            self.dst = preparation["dst"]
            self.ingress = preparation["ingress"]
            self.match = preparation["match"]
            self.path_exp = preparation["path_exp"]
            # self.all_paths = preparation["all_paths"]
            for path in preparation["all_paths"]:
                path = path.split(',')
                self.all_paths.append(path)
            while self.all_paths.__len__() != 0:
                shortest_path = min(self.all_paths, key=len)
                if shortest_path.__len__() == 0:
                    self.sum_result = 0
                    break
                print(shortest_path)
                self.sum_result = 1
                G = Network(shortest_path, self.file_path)
                classification = classify_nodes(G)
                print("Regional allocation:")
                for area_man, area in classification.items():
                    print(f"{area_man}: {area}")
                tasks = assign_tasks(G, classification)
                threads = []
                result_queue = queue.Queue()
                wrong_node_queue = queue.Queue()
                print("Task allocation:")
                for area_man, area in tasks.items():
                    print(f"{area_man}: {area}")
                    t = threading.Thread(target=verification,
                                         args=(area, self.address, result_queue, wrong_node_queue, self.file_path))
                    threads.append(t)
                    t.start()
                for t in threads:
                    t.join()
                results = []
                while not result_queue.empty():
                    results.append(result_queue.get())
                while not wrong_node_queue.empty():
                    # 打印所有结果
                    specific_edge = (wrong_node_queue.get(), wrong_node_queue.get())
                    self.all_paths = [path for path in self.all_paths if specific_edge not in zip(path[:-1], path[1:])]
                for result in results:
                    self.sum_result = self.sum_result * result
                if self.sum_result == 1:
                    print("Verification successful")
                    # 指定文件路径
                    path_num = path_num + 1
                    if path_num > 1:
                        return "false"
                    # return "true"
                else:
                    print("Verification failed")
        if self.sum_result == 1:
            return "true"
        else:
            return "false"
