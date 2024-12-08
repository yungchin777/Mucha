from muchabase import MuchaBase
import pickle
import logging

class FedClient(MuchaBase):
    def __init__(self, mode="client", config=None):
        self.config = config
        self.subscriber = MuchaBase(mode=mode, conn_info=self.config["conn_info"][0], socket_type="SUB")
        self.dealer = MuchaBase(mode=mode, conn_info=self.config["conn_info"][1], socket_type="DEALER")

    def doing(self):
        for i in range(5):
            payload = {"action": "register", "data": "123456"}
            self.dealer.send([b"", pickle.dumps(payload)])       
            response = self.dealer.recieve()
            print(f"Received: {response[-1].decode()}")

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
    fedclient.doing()

if __name__ == "__main__":
    main()
