from nicegui import ui
from plugin_base import PluginBase
import time
import logging
from PIL import Image, ImageDraw, ImageFont
import os

# Import Waveshare library
from waveshare_epd import epd2in13b_V3

class WaveshareDisplay(PluginBase):
    def __init__(self):
        super().__init__()
        self.epd = epd2in13b_V3.EPD()
        self.epd.init()
        self.width = self.epd.height  # Note: width and height are swapped for this display
        self.height = self.epd.width
        self.black_image = Image.new('1', (self.width, self.height), 255)
        self.red_image = Image.new('1', (self.width, self.height), 255)
        self.black_draw = ImageDraw.Draw(self.black_image)
        self.red_draw = ImageDraw.Draw(self.red_image)
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)

    @property
    def name(self):
        return "Waveshare e-Paper Display"

    def run(self):
        with ui.column():
            ui.label(self.name)
            self.text_input = ui.input("Text to display")
            ui.button("Display Text", on_click=self.display_text)
            ui.button("Clear Display", on_click=self.clear_display)
            ui.button("Display Time", on_click=self.start_time_display)
            ui.button("Stop Time Display", on_click=self.stop_time_display)

    def display_text(self):
        self.clear_images()
        text = self.text_input.value
        self.black_draw.text((10, 10), text, font=self.font, fill=0)
        self.update_display()
        ui.notify("Text displayed on e-Paper")

    def clear_display(self):
        self.clear_images()
        self.update_display()
        ui.notify("Display cleared")

    def clear_images(self):
        self.black_image = Image.new('1', (self.width, self.height), 255)
        self.red_image = Image.new('1', (self.width, self.height), 255)
        self.black_draw = ImageDraw.Draw(self.black_image)
        self.red_draw = ImageDraw.Draw(self.red_image)

    def update_display(self):
        self.epd.display(self.epd.getbuffer(self.black_image), self.epd.getbuffer(self.red_image))

    async def display_time(self):
        self.clear_images()
        current_time = time.strftime("%H:%M:%S")
        self.black_draw.text((10, 10), current_time, font=self.font, fill=0)
        self.update_display()

    def start_time_display(self):
        self.add_timed_event(1, self.display_time)  # Update time every second
        ui.notify("Time display started")

    def stop_time_display(self):
        self.stop_timed_events()
        ui.notify("Time display stopped")

    def cleanup(self):
        super().cleanup()
        self.epd.init()
        self.epd.Clear()
        self.epd.sleep()

def setup():
    return WaveshareDisplay()
