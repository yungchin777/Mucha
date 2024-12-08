import zmq
import uuid

class MuchaBase:
    def __init__(self, mode="server", conn_info = None, socket_type = None):
        self.socket = self.init_socket(mode, conn_info, socket_type)

    def init_socket(self, mode="server", conn_info = None, socket_type = None):
        context = zmq.Context()

        if mode not in ["server", "client"]:
            raise ValueError("Invalid mode! Use 'server' or 'client'")
        elif conn_info is None:
            raise ValueError("Connection info is empty !!!")
        elif socket_type not in ["ROUTER", "DEALER", "PUB", "SUB"]:
            raise ValueError("Aceept Value is [ROUTER, DEALER, PUB, SUB]")
        
        if mode == "server" and socket_type == "ROUTER":
            socket = context.socket(zmq.ROUTER)
            socket.setsockopt(zmq.LINGER, 0)
            socket.bind(conn_info)

        elif mode == "server" and socket_type == "PUB":
            socket = context.socket(zmq.PUB)
            socket.bind(conn_info)

        elif mode == "client" and socket_type == "DEALER":
            socket = context.socket(zmq.DEALER)
            socket.setsockopt(zmq.LINGER, 0)
            socket.setsockopt(zmq.IDENTITY, str(uuid.uuid4()).encode())
            socket.connect(conn_info)

        elif mode == "client" and socket_type == "SUB":
            socket = context.socket(zmq.SUB)
            socket.setsockopt_string(zmq.SUBSCRIBE, "")
            socket.connect(conn_info)            

        return socket
    
    def send(self, data):
        self.socket.send_multipart(data)

    def recieve(self):
        return self.socket.recv_multipart()

    def close(self):
        self.socket.close()