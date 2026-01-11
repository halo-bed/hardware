import RPi.GPIO as GPIO

MOSFET_PIN_GLOBAL = None
PWM = None


def setup_gpio(pir_pin: int, mosfet_pin: int):
    global MOSFET_PIN_GLOBAL, PWM

    MOSFET_PIN_GLOBAL = mosfet_pin

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pir_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(mosfet_pin, GPIO.OUT)

    # PWM for brightness control (1000Hz is usually fine)
    PWM = GPIO.PWM(mosfet_pin, 1000)
    PWM.start(0)  # start off


def read_motion(pir_pin: int) -> bool:
    return GPIO.input(pir_pin) == GPIO.HIGH


def set_brightness(percent: int):
    global PWM
    if PWM is None:
        return
    PWM.ChangeDutyCycle(percent)


def led_off():
    set_brightness(0)


def cleanup_gpio():
    global PWM
    try:
        if PWM is not None:
            PWM.ChangeDutyCycle(0)
            PWM.stop()
    finally:
        GPIO.cleanup()

