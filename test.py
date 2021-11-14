import serial
import paho.mqtt.client as mqtt
import ssl
import threading

ser=serial.Serial('/dev/ttyACM2',115200)

class SubThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        client = connect()
        subscribe(client)
        client.loop_forever()

class PubThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        client = connect()
        client.loop_start()
        publish(client)        

def connect():
    client = mqtt.Client()
    client.tls_set(ca_certs="ca.crt", certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
        tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

    client.connect("192.168.137.1", 8883, 60)
    return client


def subscribe(client: mqtt):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic ")

    client.subscribe("device/alarm")
    client.on_message = on_message
    

def publish(client):
    while True:
        readedText = ser.readline()
        val = readedText.strip().decode("utf-8")
        result = client.publish("device/rssi",val)


thread1 = SubThread()
thread2 = PubThread()

thread1.start()
thread2.start()







