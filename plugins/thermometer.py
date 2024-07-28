# plugins/gpio_thermometer.py
from app import PluginBase
import logging
import Adafruit_DHT

logger = logging.getLogger(__name__)

class Plugin(PluginBase):
    def __init__(self, app):
        super().__init__(app)
        self.sensor = Adafruit_DHT.DHT22
        self.pin = 4  # GPIO pin number
        logger.info("GPIO Thermometer plugin initialized")

    async def tick(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        if humidity is not None and temperature is not None:
            logger.info(f"Temp={temperature:.1f}°C  Humidity={humidity:.1f}%")
        else:
            logger.warning("Failed to retrieve data from DHT sensor")