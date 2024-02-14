import paho.mqtt.client as mqtt
import json
import ssl
import threading

aws_host = "a12ynynm96xfyz-ats.iot.us-east-1.amazonaws.com"
out_topic_aws = "device" # Este es el topicos al cual se envia en el iot core
in_topic_aws = "in_topic" # Este es el topico desde el cual se recibe
port = 8883 # Este es el puerto de iot.


edge_host = "192.168.5.199" # Este es el host de mi entorno local edge_computing
in_topic_iot = "light"  # Este es el topico con los datos que me envia el esp8266
out_topic_iot = "iot_in" # Este es el topico que envio al esp8266.

ca_path = "./certificados/AmazonRootCA1.pem"
cert_path = "./certificados/4637e4d3ae5d829877ab46d2895b4f356e2a666fba68992e41766ff52c0aa4ad-certificate.pem.crt"
key_path = "./certificados/4637e4d3ae5d829877ab46d2895b4f356e2a666fba68992e41766ff52c0aa4ad-private.pem.key"



def on_messageFromAws(client_1, userdata, message):
    payload_variable = message.payload.decode('utf-8')
    client_iot.publish("iot_in", payload_variable)
    #client.publish("device/25/data", payload=payload_variable)
    print(f"Mensaje recibido de AWS en el tema {message.topic}: {message.payload.decode('utf-8')}")


def on_messageFromESP(client, userdata, message):
    payload_variable = message.payload.decode('utf-8')
    client.publish(out_topic_aws, "1234")
    print(f"Mensaje recibido del ESP8266 en el tema {message.topic}: {message.payload.decode('utf-8')}")
    
	
 
client = mqtt.Client(protocol=mqtt.MQTTv5)
client.tls_set(ca_path, certfile=cert_path, keyfile=key_path, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)
client.connect(aws_host, port, 60)
client.on_message = on_messageFromAws
client.subscribe(in_topic_aws)

client_iot = mqtt.Client()
client_iot.connect(broker_edge, 1883)
client_iot.on_message = on_messageFromESP
client_iot.subscribe("light")


def loop_forever_iot():
    client_iot.loop_forever()

def loop_forever_aws():
    client.loop_forever()



try:
    thread1 = threading.Thread(target=loop_forever_iot)
    thread2 = threading.Thread(target=loop_forever_aws)

    # Iniciar los hilos
    thread2.start()
    thread1.start()

    # Esperar a que los hilos finalicen
    thread1.join()
    thread2.join()

except KeyboardInterrupt:
    print("Ctrl+C detectado. Cerrando el programa...")
    client.disconnect()
    client_iot.disconnect()
    thread1.join()
    thread2.join()
    print("Programa cerrado exitosamente.")



"""
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT")
        client.subscribe("light")
    else:
        print(f"Error de conexión - Código: {rc}")

def on_message(client, userdata, msg):
    print(f"Mensaje recibido en el tema '{msg.topic}': {msg.payload.decode()}")

if __name__ == "__main__":
    # Configuración del cliente MQTT
    broker_address = "192.168.5.199"
    broker_port = 1883

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Conexión al broker
    client.connect(broker_address, broker_port, 60)

    # Mantener el script en ejecución
    client.loop_start()

    try:
        while True:
            # Enviar un mensaje al tema "light"
            message = input("Ingrese el mensaje a enviar al tema 'light': ")
            client.publish("light", message)
            print(f"Mensaje enviado al tema 'light': {message}")
    except KeyboardInterrupt:
        print("Cerrando el cliente MQTT")
        client.loop_stop()
        client.disconnect()        
"""
