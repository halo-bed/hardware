import RPi.GPIO as GPIO

MOSFET_PIN_GLOBAL = None


def setup_gpio(pir_pin: int, mosfet_pin: int):
    global MOSFET_PIN_GLOBAL

    MOSFET_PIN_GLOBAL = mosfet_pin

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pir_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(mosfet_pin, GPIO.OUT)
    GPIO.output(mosfet_pin, GPIO.LOW)


def read_motion(pir_pin: int) -> bool:
    return GPIO.input(pir_pin) == GPIO.HIGH


def led_on():
    GPIO.output(MOSFET_PIN_GLOBAL, GPIO.HIGH)


def led_off():
    GPIO.output(MOSFET_PIN_GLOBAL, GPIO.LOW)


def cleanup_gpio():
    if MOSFET_PIN_GLOBAL is not None:
        GPIO.output(MOSFET_PIN_GLOBAL, GPIO.LOW)
    GPIO.cleanup()

