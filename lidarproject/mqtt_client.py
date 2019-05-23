import paho.mqtt.client as mqtt
import json


def on_connect(client, userdata, flags, rc):
    client.subscribe("scan_ready")
    print("mqtt client connected")


def on_message(client, userdata, msg):
    if msg.topic == "scan_ready":
        print("doszlo!!!!")
        json_data = json.loads(msg.payload)
        print(json_data)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.50", 1883, 60)
