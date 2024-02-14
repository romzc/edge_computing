import paho.mqtt.client as mqtt
import json
import ssl
import threading


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

