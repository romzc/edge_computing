from PubSubClient import PubSubClient


client = PubSubClient(
    out_topic="device/25/data",
    in_topic="in_topic",
    ca_path=ca_path,
    cert_path=cert_path,
    host=aws_host,
    key_path=key_path,
)


client.start()