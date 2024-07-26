from nicegui import ui
import RPi.GPIO as GPIO
from plugin_base import PluginBase
from logger_config import plugin_logger

LED_PIN = 18
PWM_FREQUENCY = 100  # Hz

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    pwm = GPIO.PWM(LED_PIN, PWM_FREQUENCY)
    pwm.start(0)  # Start with 0% duty cycle (LED off)
    plugin_logger.info("LED Control plugin setup complete")
    return LEDControl(pwm)

class LEDControl(PluginBase):
    def __init__(self, pwm):
        super().__init__()
        self.pwm = pwm
        self.state = False
        self.brightness = 0
        self.blink_task = None

    @property
    def name(self):
        return "LED Control"

    def run(self):
        with ui.column():
            ui.label(self.name)
            self.switch = ui.switch('LED', on_change=self.toggle_led)
            self.slider = ui.slider(min=0, max=100, value=0, on_change=self.set_brightness)
            self.slider.disable()
            ui.button('Start Blinking', on_click=self.start_blinking)
            ui.button('Stop Blinking', on_click=self.stop_blinking)
        plugin_logger.info("LED Control UI setup complete")

    def toggle_led(self, state):
        self.state = state
        if self.state:
            self.slider.enable()
            self.pwm.ChangeDutyCycle(self.brightness)
            plugin_logger.info(f"LED turned on, brightness: {self.brightness}%")
        else:
            self.slider.disable()
            self.pwm.ChangeDutyCycle(0)
            plugin_logger.info("LED turned off")
        ui.notify(f'LED {"on" if self.state else "off"}')

    def set_brightness(self, value):
        if self.state:
            self.brightness = value
            self.pwm.ChangeDutyCycle(self.brightness)
            plugin_logger.info(f"LED brightness set to {self.brightness}%")
            ui.notify(f'LED brightness set to {self.brightness}%')

    async def blink(self):
        self.state = not self.state
        self.pwm.ChangeDutyCycle(self.brightness if self.state else 0)
        plugin_logger.debug(f"LED blink state: {'on' if self.state else 'off'}")

    def start_blinking(self):
        self.add_timed_event(1, self.blink)  # Blink every 1 second
        plugin_logger.info("LED blinking started")
        ui.notify('LED blinking started')

    def stop_blinking(self):
        self.stop_timed_events()
        plugin_logger.info("LED blinking stopped")
        ui.notify('LED blinking stopped')

    def cleanup(self):
        super().cleanup()
        self.pwm.stop()
        GPIO.cleanup(LED_PIN)
        plugin_logger.info("LED Control plugin cleaned up")
