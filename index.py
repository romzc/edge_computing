from PubSubClient import PubSubClient

aws_host = "a12ynynm96xfyz-ats.iot.us-east-1.amazonaws.com"
aws_port = 8883
ca_path = "./certificados/AmazonRootCA1.pem"
cert_path = "./certificados/4637e4d3ae5d829877ab46d2895b4f356e2a666fba68992e41766ff52c0aa4ad-certificate.pem.crt"
key_path = "./certificados/4637e4d3ae5d829877ab46d2895b4f356e2a666fba68992e41766ff52c0aa4ad-private.pem.key"


client = PubSubClient(
    out_topic="device/25/data",
    in_topic="in_topic",
    ca_path=ca_path,
    cert_path=cert_path,
    host=aws_host,
    key_path=key_path,
)


client.start()