class Client:
    def __init__(self, address, client_socket):
        self.address = address
        self.client_socket = client_socket

    def get_address(self):
        return self.address

    def get_client_socket(self):
        return self.client_socket
