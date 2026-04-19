import time
import random
import math
import json
import joblib
import paho.mqtt.client as mqtt

BROKER = "mqtt"
PORT = 1883

DATA_TOPIC = "sensors/group20/hvac-blower/data"
ALERT_TOPIC = "alerts/group20/hvac-blower/status"

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

model = joblib.load("fan_anomaly_model.pkl")

history = []
t = 0

while True:
    base = 3.0 + 0.3 * math.sin(t / 10)
    noise = random.uniform(-0.1, 0.1)
    drift = 0.001 * t

    current = base + noise + drift

    if random.random() < 0.05:
        current += random.uniform(0.8, 1.5)

    if 80 < t < 110:
        current += 1.0

    history.append(current)
    if len(history) > 5:
        history.pop(0)

    moving_avg = sum(history) / len(history)

    prediction = model.predict([[current, moving_avg]])

    if prediction[0] == 1:
        status = "NORMAL"
        message = "Fan operating normally"
    else:
        status = "ANOMALY"
        message = "Anomalous blower fan behavior detected"

    sensor_payload = {
        "timestamp": time.time(),
        "device": "fan01",
        "current": round(current, 2),
        "moving_avg": round(moving_avg, 2),
        "unit": "A"
    }

    alert_payload = {
        "timestamp": time.time(),
        "device": "fan01",
        "status": status,
        "message": message
    }

    client.publish(DATA_TOPIC, json.dumps(sensor_payload))
    client.publish(ALERT_TOPIC, json.dumps(alert_payload))

    print("DATA :", sensor_payload)
    print("ALERT:", alert_payload)
    print("-" * 50)

    t += 1
    time.sleep(2)