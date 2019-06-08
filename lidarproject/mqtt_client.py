import paho.mqtt.client as mqtt
import json
from django.contrib import messages
from django.shortcuts import redirect

from main.models import SingleScanResult, TestScenario


def on_connect(client, userdata, flags, rc):
    client.subscribe("scan_ready")
    print("mqtt client connected")


def on_message(client, userdata, msg):
    if msg.topic == "scan_ready":
        print("doszlo!!!!")
        json_data = json.loads(msg.payload)
        scenario_id = json_data["scenario_id"]
        scenario = TestScenario.objects.filter(id=scenario_id)[0]
        tests = json_data["results"]
        for t in tests:
            delay = float(t["delay"])
            mode = int(t["mode"])
            measurements = t["measurements"]
            scan_time = float(t["scan_time"])
            missed_steppes_scan = int(t["missed_steppes_scan"])
            missed_steppes_return = int(t["missed_steppes_return"])
            single_scan_result = SingleScanResult(delay=delay, mode=mode, scenario=scenario, measurements=measurements,
                                                  scan_time=scan_time, missed_steppes_scan=missed_steppes_scan,
                                                  missed_steppes_return=missed_steppes_return)
            single_scan_result.save()

        # messages.info("Pomiary zakończone!")
        return redirect("main:boards")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.50", 1883, 60)
