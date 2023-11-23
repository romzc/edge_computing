import paho.mqtt.client as mqtt
import ssl
from time import sleep
import json

class PubSubClient:
    _connect : bool
    _topic: str
    _cert_path: str
    _key_path: str
    _ca_path: str
    _host: str
    _out_topic: str
    
    
    def __init__(self, in_topic: str, out_topic: str, ca_path: str, cert_path: str, key_path: str, host: str) -> None:
        self._connect = False
        self._in_topic = in_topic
        self._out_topic = out_topic
        self._cert_path = cert_path
        self._key_path = key_path
        self._ca_path = ca_path
        self._host = host
        self._client = None
    
    def _on_connect(self, client, user_data, flags, rc, properties=None) -> None:
        self._connect = True
        print(f"conectado con resultado: {rc}")
        client.subscribe(self._in_topic)
        
    
    def _on_message(self, client, use_data, msg) -> None:
        print(f"{msg.topic} {msg.payload}")
    
    
    def _setup_mqtt(self) -> None:
        self._client = mqtt.Client(protocol=mqtt.MQTTv5)
        self._client.tls_set(self._ca_path,
            certfile=self._cert_path,
            keyfile=self._key_path,
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLSv1_2,
            ciphers=None)

        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        
        result: int = self._client.connect(self._host, 8883, 60)
        
        if result == 0:
            self._connect = True
        
            
    def stop(self):
        self._client.loop_stop()
        self._connect = False
    
        
    def publish(self, value: dict):
        if self._connect:
            self._client.publish(self._out_topic, json.dumps(value), qos=1)
        else:
            raise Exception("mqtt client is not connected")     
    
    
    def start(self) -> None:
        self._setup_mqtt()
        self._client.loop_start()
        
        while self._connect:
            sleep(2)
            if self._connect == True:
                self.publish(value={"message": "Hello from romzc"})

        