from muchabase import MuchaBase
import time
import threading
import logging
from queue import Queue
import torch
import torchvision.models as models
from utils import load_custom_models

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

                    payload = [client_id, msg]
                    self.router.send(payload)
                else:
                    msg = f"{client_id} already exists"

                    logging.info(msg)

                    payload = [client_id, msg]
                    self.router.send(payload)

    def uploaded_model(self):
        while True:
            if not self.upload_model_queue.empty():
                client_id, model_parameters = self.upload_model_queue.get()
                self.client_ids[client_id] = model_parameters

    def publish_model(self):
        model_name = self.config["model_name"]
        pretrained = self.config["pretrained"]
        model = load_custom_models.load_model_from_config(model_name, self.config, pretrained)
        print(model)
        # available_models = models._api.list_models()

        # try:
        #     model = models._api.get_model(model_name, weights="DEFAULT" if pretrained else None)
        
        # except Exception as e:
        #     raise ValueError(
        #         f"Error: Model '{model_name}' is not available in torchvision. \n"
        #         f"Available models: {available_models}"
        #     )

    def aggregate_model(self):
        pass

    def msg_handler(self, msg):
        client_id, payload = msg

        if payload["action"] == "register":
            self.register_queue.put(client_id)
        
        if payload["action"] == "upload":
            self.upload_model_queue.put((client_id, payload["data"]))

    def run(self):
        # threading.Thread(target=self.register_client, daemon=True).start()
        # threading.Thread(target=self.publish_model, daemon=True).start()
        # threading.Thread(target=self.uploaded_model, daemon=True).start()

        # while True:
        #     msg = self.router.recv()
        #     self.msg_handler(msg)
        self.publish_model()


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
    config["model_name"] = "mymodel"
    config["pretrained"] = True
    config["class"] = 10

    fedserver = FedServer(mode=mode, config=config)
    fedserver.run()

if __name__ == "__main__":
    main()