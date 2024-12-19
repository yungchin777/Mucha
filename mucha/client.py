from muchabase import MuchaBase
import logging
import torch

class FedClient:
    def __init__(self, mode="client", config=None):
        self.config = config
        self.subscriber = MuchaBase(mode=mode, conn_info=self.config["conn_info"][0], socket_type="SUB")
        self.dealer = MuchaBase(mode=mode, conn_info=self.config["conn_info"][1], socket_type="DEALER")
        self.init_model = None

    def register_server(self):
        payload = {"action": "register", "data": ""}
        self.dealer.send(["", payload])
        rep = self.dealer.recv()
        logging.info(f"Receive msg: {rep}")

    def recv_init_model(self):
        rep = self.subscriber.recv()
        self.init_model = rep

def main():
    mode = "client"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler()
        ]
    )

    logging.info("Initializing FedClient ...")

    config = {}
    config["conn_info"] = ["tcp://127.0.0.1:5555", "tcp://127.0.0.1:6666"]

    fedclient = FedClient(mode=mode, config=config)
    fedclient.register_server()

if __name__ == "__main__":
    main()
