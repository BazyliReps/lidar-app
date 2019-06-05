import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
from single_scan import turn
from datetime import datetime
from stepper_utils import calibrate, turn_stepper_on, set_stepper_mode
import RPi.GPIO as GPIO
from time import sleep


def on_connect(client, userdata, flags, rc):
    print("connecting...")
    client.subscribe("make_scan")
    print("connected!")


def on_message(client, userdata, msg):
    print(msg.topic)
    if msg.topic == "make_scan":
        payload = json.loads(msg.payload.decode('utf-8'))
        scenario_id = payload["id"]
        tests = payload["tests"]
        results = []
        
        turn_stepper_on()

        calibrate(0.001, 0.01)

        for t in tests:
            delay = float(t["delay"])
            mode = int(t["operating_mode"])
            reps = int(t["repetitions"])
            for r in range(reps):
                start_time = datetime.now()
                measurements,missed_steppes_scan,missed_steppes_return = turn(mode, delay)
                measurements = json.dumps(measurements)
                stop_time = datetime.now()
                scan_time = (stop_time - start_time).total_seconds()
                print("czas skanu: %f" %(scan_time))
                results.append({"delay": delay, "mode": mode, "measurements": measurements, "scan_time": scan_time, 
                    "missed_steppes_scan": missed_steppes_scan, "missed_steppes_return": missed_steppes_return})

        return_data = json.dumps({"scenario_id": scenario_id, "results": results})
        publish.single("scan_ready", return_data, hostname="192.168.0.50")
        print("scan ready!")
        GPIO.output(16, GPIO.LOW)



client = mqtt.Client()
print("after clent")
client.on_connect = on_connect
client.on_message = on_message
print("before connect")
client.connect("192.168.0.50", 1883, 60)

client.loop_forever()


