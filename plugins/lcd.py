# plugins/raspberry_lcd.py
from app import PluginBase
import logging
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

logger = logging.getLogger(__name__)

class Plugin(PluginBase):
    def __init__(self, app):
        super().__init__(app)
        # Modify these as needed for your LCD setup
        lcd_columns = 16
        lcd_rows = 2
        lcd_rs = digitalio.DigitalInOut(board.D26)
        lcd_en = digitalio.DigitalInOut(board.D19)
        lcd_d4 = digitalio.DigitalInOut(board.D13)
        lcd_d5 = digitalio.DigitalInOut(board.D6)
        lcd_d6 = digitalio.DigitalInOut(board.D5)
        lcd_d7 = digitalio.DigitalInOut(board.D11)
        self.lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
        logger.info("Raspberry LCD Display plugin initialized")

    async def tick(self):
        # Update LCD display here if needed
        pass

    def display_message(self, message):
        self.lcd.clear()
        self.lcd.message = message
        logger.info(f"Displayed message on LCD: {message}")