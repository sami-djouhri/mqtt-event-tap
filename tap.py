"""
MQTT Event Tap, konsumiert `homelab/#` und loggt jede Message als strukturiertes JSON.
Gedacht als Live-Tap + Future Data-Source für Loki/Grafana Logs.
"""

import json
import os
import sys

import paho.mqtt.client as mqtt
import structlog

MQTT_HOST = os.environ.get("MQTT_HOST", "mosquitto")
MQTT_PORT = int(os.environ.get("MQTT_PORT", "1883"))
MQTT_USERNAME = os.environ.get("MQTT_USERNAME")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")
MQTT_PASSWORD_FILE = os.environ.get("MQTT_PASSWORD_FILE")
if MQTT_PASSWORD_FILE and os.path.exists(MQTT_PASSWORD_FILE):
    with open(MQTT_PASSWORD_FILE) as f:
        MQTT_PASSWORD = f.read().strip()
TOPIC = os.environ.get("TOPIC", "homelab/#")

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.add_log_level,
        structlog.processors.EventRenamer("msg"),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.PrintLoggerFactory(),
)
log = structlog.get_logger("mqtt-event-tap")


def on_connect(client, userdata, flags, reason_code, properties=None):
    log.info("connected", host=MQTT_HOST, port=MQTT_PORT, reason=str(reason_code))
    client.subscribe(TOPIC)
    log.info("subscribed", topic=TOPIC)


def on_message(client, userdata, msg):
    parts = msg.topic.split("/")
    # homelab/{service}/{entity}/{action}
    service = parts[1] if len(parts) > 1 else "?"
    entity = parts[2] if len(parts) > 2 else "?"
    action = parts[3] if len(parts) > 3 else "?"

    try:
        payload = json.loads(msg.payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        payload = {"_raw": msg.payload.decode("utf-8", errors="replace")}

    log.info(
        "event",
        topic=msg.topic,
        service=service,
        entity=entity,
        action=action,
        retain=bool(msg.retain),
        qos=msg.qos,
        payload=payload,
    )


def main() -> int:
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id="mqtt-event-tap",
    )
    if MQTT_USERNAME:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()
    return 0


if __name__ == "__main__":
    sys.exit(main())
