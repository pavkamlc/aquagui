# plugins/gpio_dimable_led.py
from app import PluginBase
import logging
import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)

class Plugin(PluginBase):
    def __init__(self, app):
        super().__init__(app)
        self.led_pin = 18  # GPIO pin number
        self.pwm_frequency = 100  # Hz
        self.duty_cycle = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.led_pin, self.pwm_frequency)
        self.pwm.start(self.duty_cycle)
        logger.info("GPIO Dimable LED plugin initialized")

    async def tick(self):
        # You can implement automatic dimming logic here if needed
        pass

    def set_brightness(self, brightness):
        self.duty_cycle = brightness
        self.pwm.ChangeDutyCycle(self.duty_cycle)
        logger.info(f"LED brightness set to {brightness}%")

    def __del__(self):
        self.pwm.stop()
        GPIO.cleanup()