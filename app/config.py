import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "").rstrip("/")

#GPIO
PIR_PIN = int(os.getenv("PIR_PIN", 16))
MOSFET_PIN = int(os.getenv("MOSFET_PIN", 17))

# Timing
WARMUP_SECONDS = int(os.getenv("WARMUP_SECONDS", 30))
LOOP_DELAY = float(os.getenv("LOOP_DELAY", 0.1))

# Defaults
DEFAULT_AUTO_OFF = int(os.getenv("DEFAULT_AUTO_OFF", 30))
DEFAULT_BRIGHTNESS = int(os.getenv("DEFAULT_BRIGHTNESS", 100))

# PubNub
PUBNUB_PUBLISH_KEY = os.getenv("PUBNUB_PUBLISH_KEY")
PUBNUB_SUBSCRIBE_KEY = os.getenv("PUBNUB_SUBSCRIBE_KEY")
PUBNUB_UUID = os.getenv("PUBNUB_UUID", "raspi-pir-01")
DEVICE_KEY = os.getenv("DEVICE_KEY", "")

PUBNUB_EVENTS_CHANNEL = os.getenv("PUBNUB_EVENTS_CHANNEL", "pir-events")
PUBNUB_CONTROL_CHANNEL = os.getenv("PUBNUB_CONTROL_CHANNEL", "pir-control")

def validate():
    if not BACKEND_BASE_URL:
        raise ValueError("BACKEND_BASE_URL is missing in .env")
    if not DEVICE_KEY:
        raise ValueError("DEVICE_KEY is missing in .env")
    if not PUBNUB_PUBLISH_KEY or not PUBNUB_SUBSCRIBE_KEY:
        raise ValueError("PUBNUB_PUBLISH_KEY / PUBNUB_SUBSCRIBE_KEY missing in .env")


