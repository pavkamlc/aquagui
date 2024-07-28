# plugins/epaper_display.py
from app import PluginBase
import logging
from waveshare_epd import epd2in13_V2
import time

logger = logging.getLogger(__name__)

class Plugin(PluginBase):
    def __init__(self, app):
        super().__init__(app)
        self.epd = epd2in13_V2.EPD()
        self.epd.init(self.epd.FULL_UPDATE)
        self.epd.Clear(0xFF)
        logger.info("E-Paper Display plugin initialized")

    async def tick(self):
        # Update e-paper display here if needed
        pass

    def display_image(self, image):
        self.epd.display(self.epd.getbuffer(image))
        logger.info("Displayed image on E-Paper")

    def __del__(self):
        self.epd.sleep()