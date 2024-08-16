import ipaddress


class Fwd:

    def __init__(self, device, network_path):
        self.device = device
        self.fwd = []
        self.network_path = network_path
        self.fw_table = []
        self.set_fwd()

    def get_device(self):
        return self.device

    def get_fwd(self):
        return self.fwd

    def set_fwd(self):
        file_path = self.network_path + "/rule/" + str(self.device)
        with open(file_path, "r") as file:
            # 逐行读取文件内容并存储到数组中
            message = file.readlines()
        for string in message:
            string = string.strip()
            fwd_table = string.split(" ")
            # index = 1
            address = []
            prefix = []
            forward = []
            address.append(fwd_table[1])
            prefix.append(fwd_table[2])
            forward.append(fwd_table[3].split('->')[1])
            self.fwd.append({"address": address, "prefix": prefix, "forward": forward})

    def parse_fwd(self):
        entries = []
        for fw in self.fwd:
            ip_decimal = int(str(fw["address"][0]))
            prefix = int(str(fw["prefix"][0]))
            dest = fw["forward"][0]
            entries.append((ip_decimal, prefix, dest))
        return entries

    def calculate_ip_range(self, ip_decimal, prefix):
        network = ipaddress.ip_network((ip_decimal, prefix), strict=False)
        return (int(network.network_address), int(network.broadcast_address))

    def group_by_destination(self, entries):
        groups = {}
        for ip_decimal, prefix, dest in entries:
            if dest not in groups:
                groups[dest] = []
            ip_range = self.calculate_ip_range(ip_decimal, prefix)
            groups[dest].append(ip_range)
        return groups

    def merge_ranges(self, ranges):
        # 将范围按起始地址排序
        ranges.sort()
        merged = []
        current_start, current_end = ranges[0]
        for start, end in ranges[1:]:
            if start <= current_end + 1:
                current_end = max(current_end, end)
            else:
                merged.append((current_start, current_end))
                current_start, current_end = start, end
        merged.append((current_start, current_end))
        return merged


# if __name__ == '__main__':
#     device = Fwd("S")
#     # device.set_device()
#     device.set_fwd()
#     entries = device.get_fwd()
