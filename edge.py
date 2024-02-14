import paho.mqtt.client as mqtt
import json
import ssl
import threading
import time

last_message_time = 0

aws_host = "a12ynynm96xfyz-ats.iot.us-east-1.amazonaws.com"
out_topic_aws = "device/25/data"  # Este es el tópico al cual se envía en el AWS IoT Core
in_topic_aws = "in_topic"  # Este es el tópico desde el cual se recibe
port = 8883  # Este es el puerto de AWS IoT Core

edge_host = "192.168.255.104"  # Este es el host de tu entorno local de edge computing
in_topic_iot = "light"  # Este es el tópico con los datos que envía el ESP8266
out_topic_iot = "iot_in"  # Este es el tópico que envía al ESP8266.

ca_path = "./certificados/AmazonRootCA1.pem"
cert_path = "./certificados/4637e4d3ae5d829877ab46d2895b4f356e2a666fba68992e41766ff52c0aa4ad-certificate.pem.crt"
key_path = "./certificados/4637e4d3ae5d829877ab46d2895b4f356e2a666fba68992e41766ff52c0aa4ad-private.pem.key"


def on_message_from_aws(client, userdata, message):
    payload_variable = message.payload.decode('utf-8')
    print(f"Mensaje recibido de AWS en el tópico {message.topic}: {payload_variable}")
    client_iot.publish(out_topic_iot, payload_variable)
    

def on_message_from_iot(client, userdata, message):
    global last_message_time
    payload_variable = message.payload.decode('utf-8')
    response_dictionary = json.loads(payload_variable)
    current_time = time.time()
    if current_time - last_message_time >= 10 or response_dictionary["motion"] == 1:
        # formatear los datos el formato
        format_data = {"light": response_dictionary["light"], "motion": response_dictionary["motion"]}
        json_to_send = json.dumps(format_data)
        print(json_to_send)
        client_aws.publish(out_topic_aws, json_to_send)        
        last_message_time = current_time



client_aws = mqtt.Client(protocol=mqtt.MQTTv5)
client_aws.tls_set(ca_path, certfile=cert_path, keyfile=key_path, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)
client_aws.on_message = on_message_from_aws
client_aws.connect(aws_host, port, 60)
client_aws.subscribe(in_topic_aws)

client_iot = mqtt.Client()
client_iot.on_message = on_message_from_iot
client_iot.connect(edge_host, 1883)
client_iot.subscribe(in_topic_iot)


def loop_forever_aws():
    client_aws.loop_forever()

def loop_forever_iot():
    client_iot.loop_forever()

try:
    thread1 = threading.Thread(target=loop_forever_aws)
    thread2 = threading.Thread(target=loop_forever_iot)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

except KeyboardInterrupt:
    print("Ctrl+C detectado. Cerrando el programa...")
    client_aws.disconnect()
    client_iot.disconnect()
    thread1.join()
    thread2.join()
    print("Programa cerrado exitosamente.")