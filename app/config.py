import os
from dotenv import load_dotenv

load_dotenv()

# GPIO
PIR_PIN = int(os.getenv("PIR_PIN", 16))
MOSFET_PIN = int(os.getenv("MOSFET_PIN", 17))

# Timing
WARMUP_SECONDS = int(os.getenv("WARMUP_SECONDS", 30))
ON_SECONDS = int(os.getenv("ON_SECONDS", 30))
LOOP_DELAY = float(os.getenv("LOOP_DELAY", 0.1))

# PubNub
PUBNUB_PUBLISH_KEY = os.getenv("PUBNUB_PUBLISH_KEY")
PUBNUB_SUBSCRIBE_KEY = os.getenv("PUBNUB_SUBSCRIBE_KEY")
PUBNUB_UUID = os.getenv("PUBNUB_UUID", "raspi-pir-01")
PUBNUB_CHANNEL = os.getenv("PUBNUB_CHANNEL", "pir-events")

if not PUBNUB_PUBLISH_KEY or not PUBNUB_SUBSCRIBE_KEY:
    raise ValueError("Missing PubNub keys in .env")

