from verification.device_fwd import Fwd


class Device:
    def __init__(self, name):
        self.name = name
        self.category = ""
        self.fw_table = {}
        self.port = None

    def set_category(self, category):
        self.category = category

    def get_category(self):
        return self.category

    def set_fw(self, file):
        self.fw_table = Fwd(self.name, file).get_fwd()

    def get_fw(self):
        return self.fw_table
