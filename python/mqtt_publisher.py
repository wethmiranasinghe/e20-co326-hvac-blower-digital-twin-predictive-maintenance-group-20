import time
import random
import math
import json
import joblib
import paho.mqtt.client as mqtt
import pandas as pd
import argparse
import signal
import sys
import logging
import os

def load_model(path):
    return joblib.load(path)


def create_client(broker, port, keepalive=60, max_retries=8):
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    backoff = 1
    for attempt in range(max_retries):
        try:
            client.connect(broker, port, keepalive)
            return client
        except Exception as e:
            logging.getLogger(__name__).warning("MQTT connect attempt %d failed: %s", attempt+1, e)
            time.sleep(backoff)
            backoff = min(backoff * 2, 30)
    raise ConnectionError(f"Could not connect to MQTT broker {broker}:{port}")


def run_publisher(args):
    BROKER = args.broker
    PORT = args.port
    DATA_TOPIC = args.data_topic
    ALERT_TOPIC = args.alert_topic

    client = create_client(BROKER, PORT)

    model = load_model(args.model_path)

    history = []
    t = 0

    stop_requested = False

    logger = logging.getLogger(__name__)

    def _signal_handler(sig, frame):
        nonlocal stop_requested
        logger.info("Shutdown requested")
        stop_requested = True

    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    while not stop_requested and (args.iterations is None or t < args.iterations):
        cycle_t = t % args.cycle_length

        base = 3.0 + 0.3 * math.sin(cycle_t / 10)
        noise = random.uniform(-0.1, 0.1)
        drift = 0.001 * cycle_t

        current = base + noise + drift

        if random.random() < 0.05:
            current += random.uniform(0.8, 1.5)

        if 80 < cycle_t < 110:
            current += 1.0

        history.append(current)
        if len(history) > 5:
            history.pop(0)

        moving_avg = sum(history) / len(history)

        features = pd.DataFrame([{"current": current, "moving_avg": moving_avg}])
        prediction = model.predict(features)

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

        logger.info("DATA : %s", sensor_payload)
        logger.info("ALERT: %s", alert_payload)
        logger.info("%s", "-" * 50)

        t += 1
        time.sleep(args.interval)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--broker", default=os.getenv("MQTT_BROKER_HOST", "mqtt"), help="MQTT broker host")
    parser.add_argument("--port", type=int, default=int(os.getenv("MQTT_BROKER_PORT", "1883")), help="MQTT broker port")
    parser.add_argument("--data-topic", default="sensors/group20/hvac-blower/data")
    parser.add_argument("--alert-topic", default="alerts/group20/hvac-blower/status")
    parser.add_argument("--model-path", default="fan_anomaly_model.pkl")
    parser.add_argument("--interval", type=float, default=2.0, help="Publish interval (s)")
    parser.add_argument("--iterations", type=int, default=None, help="Number of iterations to run (for testing)")
    parser.add_argument("--cycle-length", type=int, default=180, help="Simulation cycle length before drift resets")
    parser.add_argument("--log-level", default="INFO", help="Logging level (DEBUG, INFO, WARNING, ERROR)")
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO),
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    try:
        run_publisher(args)
    except Exception:
        logging.getLogger(__name__).exception("Publisher exited with error")
        sys.exit(1)


if __name__ == "__main__":
    main()
