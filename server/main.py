from socket import socket, SOCK_STREAM, AF_INET

DEFAULT_PORT = 10100


class Server:
    def prepare(self, ip_address):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((ip_address, DEFAULT_PORT))
        self.socket.listen(1)

    def start(self, ip_address):
        self.prepare(ip_address)
        # print(self.socket)
        # TODO threading
        self.connection, self.exception = self.socket.accept()


server = Server()
server.start(ip_address="localhost")
