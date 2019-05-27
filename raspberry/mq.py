import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
from single_scan import turn
from datetime import datetime

def on_connect(client, userdata, flags, rc):
    client.subscribe("make_scan")

def calibrate():
    return 0


def on_message(client, userdata, msg):
    print(msg.topic)
    if msg.topic == "make_scan":
        payload = json.loads(msg.payload)
        scenario_id = payload["id"]
        tests = payload["tests"]
        results = []
        for t in tests:
            delay = float(t["delay"])
            mode = int(t["operating_mode"])
            reps = int(t["repetitions"])
            print(reps)
            for r in range(reps):
                print("w reps")
                start_time = datetime.now()
                measurements = json.dumps(turn(mode, delay))
                stop_time = datetime.now()
                scan_time = (stop_time - start_time).total_seconds()
                print(scan_time)
                print(type(scan_time))
                missed_steppes = calibrate()
                results.append({"delay": delay, "mode": mode, "measurements": measurements, "scan_time": scan_time, "missed_steppes": missed_steppes})

        return_data = json.dumps({"scenario_id": scenario_id, "results": results})
        publish.single("scan_ready", return_data, hostname="192.168.0.50")
        print("scan ready!")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.50", 1883, 60)

client.loop_forever()


