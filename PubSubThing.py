from PubSubClient import PubSubClient


class PubSubThing(PubSubClient):
    
    def __init__(self, in_topic: str, out_topic: str, ca_path: str, cert_path: str, key_path: str, host: str) -> None:
        super().__init__(in_topic, out_topic, ca_path, cert_path, key_path, host)
        