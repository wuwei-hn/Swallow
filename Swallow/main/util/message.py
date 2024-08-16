class Message:
    def __init__(self, area):
        self.area = area
        self.result = None

    def set_result(self, result):
        self.result = result

    def get_result(self):
        return self.result
