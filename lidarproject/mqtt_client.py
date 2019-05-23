import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    client.subscribe("jeden")
    client.subscribe("cztery")
    client.subscribe("scan_ready")
    print("on connect poszlo!")


def on_message(client, userdata, msg):
    print("topic: " + msg.topic + "   payload: " + str(msg.payload))

    if msg.topic == "scan_ready":
        print("doszlo!!!!")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.50", 1883, 60)
print("after connect!")
