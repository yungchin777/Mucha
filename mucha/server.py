from muchabase import MuchaBase
import time
import pickle
import threading
import logging
from queue import Queue

class FedServer:
    def __init__(self, mode="server", config=None):
        self.config = config
        self.publisher = MuchaBase(mode=mode, conn_info=self.config["conn_info"][0], socket_type="PUB")
        self.router = MuchaBase(mode=mode, conn_info=self.config["conn_info"][1], socket_type="ROUTER")
        self.client_ids = {}
        self.register_queue = Queue()
        self.upload_model_queue = Queue()

    def register_client(self):
        while True:
            if not self.register_queue.empty():
                client_id = self.register_queue.get()

                if self.client_ids.get(client_id, -1):
                    self.client_ids[client_id] = None
                    msg = f"{client_id} register successfully"

                    logging.info(msg)

                    payload = [client_id.encode(), msg.encode()]
                    self.router.send(payload)
                else:
                    msg = f"{client_id} already exists"

                    logging.info(msg)

                    payload = [client_id.encode(), msg.encode()]
                    self.router.send(payload)

    def uploaded_model(self):
        while True:
            if not self.upload_model_queue.empty():
                client_id, model_parameters = self.upload_model_queue.get()
                self.client_ids[client_id] = model_parameters

    def publish_model(self):
        pass

    def aggregate_model(self):
        pass

    def msg_handler(self, msg):
        client_id, _, content = msg

        client_id = client_id.decode()
        payload = pickle.loads(content)

        if payload["action"] == "register":
            self.register_queue.put(client_id)
        
        if payload["action"] == "upload":
            self.upload_model_queue.put((client_id, payload["data"]))

    def run(self):
        threading.Thread(target=self.register_client, daemon=True).start()
        threading.Thread(target=self.uploaded_model, daemon=True).start()

        while True:
            msg = self.router.recieve()
            self.msg_handler(msg)

    def doing(self):
        while True:
            # 接收客戶端消息，獲取客戶端 ID
            client_message = self.router.recieve()
            client_id, empty, content = client_message
            print(client_id, empty, content)
            print(f"Received from {client_id.decode()}: {pickle.loads(content)}")

            # 回應客戶端
            response = [client_id, b"", b"Hello, Client!"]
            self.router.send(response)
            print(f"Sent: {response[-1].decode()}")
            time.sleep(1)

def main():
    mode = "server"
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler()
        ]
    )

    logging.info("Initializing FedServer...")

    config = {}
    config["conn_info"] = ["tcp://127.0.0.1:5555", "tcp://127.0.0.1:6666"]

    fedserver = FedServer(mode=mode, config=config)
    fedserver.run()

if __name__ == "__main__":
    main()