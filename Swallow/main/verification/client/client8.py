import os
import socket
import threading
import time
import tracemalloc
import psutil
from network import Network
elapsed_time = 0

def verification(data):
    tracemalloc.start()
    global elapsed_time
    graph = Network(data, '../../../dataset/i2')
    rmul = 1
    packet_space = 335544320
    devices = graph.get_devices()
    for node1, node2 in zip(data[:-1], data[1:]):
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
            return str(rmul) + "," + str(node1) + "," + str(node2)
            break

    current, peak = tracemalloc.get_traced_memory()
    memory = (peak - current) / (1024 * 1024)
    return str(rmul)

def receive_messages(client_socket):

    running = True
    while running:
        try:
            data = client_socket.recv(1024).decode()
            print(data)
            start_time = time.time()
            tracemalloc.start()

            # 获取当前进程
            process = psutil.Process(os.getpid())

            # 获取程序运行前的 CPU 时间和负载
            cpu_times_before = process.cpu_times()  # 返回一个 namedtuple，包含用户和系统 CPU 时间
            cpu_load_before = process.cpu_percent(interval=None)  # 获取当前 CPU 负载

            if not data:
                break
            if data == 'quit':
                client_socket.close()
                os._exit(0)
            print(f"Received message from server: {data}")
            global elapsed_time

            data = data.split(',')
            result = verification(data)
            client_socket.sendall(result.encode())
            running = False
            end_time = time.time()
            elapsed_time = (end_time - start_time) * 1000
            print(elapsed_time)
            current, peak = tracemalloc.get_traced_memory()
            memory = (peak - current) / (1024 * 1024)
            print(f"Memory use: {memory} MB")

            # 获取程序运行后的 CPU 时间和负载
            cpu_times_after = process.cpu_times()
            cpu_load_after = process.cpu_percent(interval=None)

            # 计算 CPU 时间差
            user_cpu_time_used = cpu_times_after.user - cpu_times_before.user
            system_cpu_time_used = cpu_times_after.system - cpu_times_before.system

            # 输出 CPU 使用时间和负载
            print(f"用户 CPU 时间: {user_cpu_time_used:.2f} 秒")
            print(f"系统 CPU 时间: {system_cpu_time_used:.2f} 秒")
            print(f"程序运行期间 CPU 负载前后变化: {cpu_load_before}% -> {cpu_load_after}%")
        except ConnectionResetError:
            break

    # client_socket.close()



def start_client(server_ip, server_port=12345):
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, server_port))
            client_socket.sendall('atla'.encode())
            t = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
            t.start()
            t.join()
            time.sleep(1)
        finally:
            client_socket.close()


if __name__ == "__main__":

    server_ip = '210.37.38.48'
    start_client(server_ip)

