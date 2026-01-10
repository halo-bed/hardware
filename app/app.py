import time
from config import (
    PIR_PIN,
    MOSFET_PIN,
    WARMUP_SECONDS,
    ON_SECONDS,
    LOOP_DELAY,
    PUBNUB_UUID,
)
from gpio_control import setup_gpio, read_motion, led_on, led_off, cleanup_gpio
from pubnub_client import publish_event


def run():
    setup_gpio(PIR_PIN, MOSFET_PIN)

    print(f"PIR warming up ({WARMUP_SECONDS}s)...")
    time.sleep(WARMUP_SECONDS)
    print("System Ready!")

    last_state = None

    try:
        while True:
            motion = read_motion(PIR_PIN)

            if motion:
                led_on()
                print("Motion Detected -> LED ON")

                if last_state != "motion":
                    publish_event(
                        {
                            "device": PUBNUB_UUID,
                            "event": "motion",
                            "state": "detected",
                            "led": "ON",
                            "ts": time.time(),
                        }
                    )
                    last_state = "motion"

                time.sleep(ON_SECONDS)

            else:
                led_off()
                print("No Motion Detected -> LED OFF")

                if last_state != "idle":
                    publish_event(
                        {
                            "device": PUBNUB_UUID,
                            "event": "motion",
                            "state": "none",
                            "led": "OFF",
                            "ts": time.time(),
                        }
                    )
                    last_state = "idle"

            time.sleep(LOOP_DELAY)

    except KeyboardInterrupt:
        print("Exiting Program")

    finally:
        cleanup_gpio()

