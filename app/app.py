import time
from config import (
    PIR_PIN,
    MOSFET_PIN,
    WARMUP_SECONDS,
    LOOP_DELAY,
    DEFAULT_AUTO_OFF,
    DEFAULT_BRIGHTNESS,
    PUBNUB_UUID,
    PUBNUB_EVENTS_CHANNEL,
    PUBNUB_CONTROL_CHANNEL,
    PUBNUB_PUBLISH_KEY,
    PUBNUB_SUBSCRIBE_KEY,
)
from gpio_control import setup_gpio, read_motion, set_brightness, led_off, cleanup_gpio
from pubnub_client import PubNubClient
from controls import ControlState


def run():
    controls = ControlState(
        auto_off=DEFAULT_AUTO_OFF,
        brightness=DEFAULT_BRIGHTNESS,
        start_time=None,
        end_time=None,
    )

    pn = PubNubClient(PUBNUB_PUBLISH_KEY, PUBNUB_SUBSCRIBE_KEY, PUBNUB_UUID)

    def handle_control_message(msg: dict):
        changed = controls.update_from_message(msg)
        if changed:
            set_brightness(controls.brightness)
            pn.publish(PUBNUB_EVENTS_CHANNEL, {
                "device": PUBNUB_UUID,
                "event": "control",
                "state": "updated",
                "controls": {
                    "auto_off": controls.auto_off,
                    "brightness": controls.brightness,
                    "start_time": controls.start_time.isoformat() if controls.start_time else None,
                    "end_time": controls.end_time.isoformat() if controls.end_time else None,
                },
                "ts": time.time(),
            })
            print("Controls updated:", msg)

    pn.subscribe(PUBNUB_CONTROL_CHANNEL, handle_control_message)
    print("Subscribed to:", PUBNUB_CONTROL_CHANNEL)

    setup_gpio(PIR_PIN, MOSFET_PIN)

    print(f"PIR warming up ({WARMUP_SECONDS}s)...")
    time.sleep(WARMUP_SECONDS)
    print("System Ready!")

    last_state = None

    try:
        while True:
            motion = read_motion(PIR_PIN)

            allowed = controls.within_allowed_window()

            if motion and allowed:
                set_brightness(controls.brightness)
                print("Motion Detected -> LED ON")

                if last_state != "motion":
                    pn.publish(PUBNUB_EVENTS_CHANNEL, {
                        "device": PUBNUB_UUID,
                        "event": "motion",
                        "state": "ON",
                        "brightness": controls.brightness,
                        "auto_off": controls.auto_off,
                        "allowed": True,
                        "ts": time.time(),
                    })
                    last_state = "motion"

                time.sleep(controls.auto_off)
                led_off()

            else:
                led_off()
                if motion and not allowed:
                    print("Motion detected but OUTSIDE time window -> LED OFF")
                else:
                    print("No Motion Detected -> LED OFF")

                if last_state != "idle":
                    pn.publish(PUBNUB_EVENTS_CHANNEL, {
                        "device": PUBNUB_UUID,
                        "event": "motion",
                        "state": "OFF",
                        "allowed": allowed,
                        "ts": time.time(),
                    })
                    last_state = "idle"

            time.sleep(LOOP_DELAY)

    except KeyboardInterrupt:
        print("Exiting Program")

    finally:
        led_off()
        cleanup_gpio()
        pn.stop()

