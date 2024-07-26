from nicegui import ui
import paho.mqtt.client as mqtt
from plugin_base import PluginBase
import json
import time

def setup():
    return MQTTClient()

class MQTTClient(PluginBase):
    def __init__(self):
        super().__init__()
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.connected = False
        self.messages = []

    @property
    def name(self):
        return "MQTT Client"

    def run(self):
        with ui.column():
            ui.label(self.name)
            self.broker = ui.input("Broker Address")
            self.port = ui.number("Port", value=1883)
            self.topic = ui.input("Topic")

            with ui.row():
                ui.button("Connect", on_click=self.connect)
                ui.button("Disconnect", on_click=self.disconnect)

            with ui.row():
                self.subscribe_topic = ui.input("Subscribe Topic")
                ui.button("Subscribe", on_click=self.subscribe)

            with ui.row():
                self.publish_topic = ui.input("Publish Topic")
                self.publish_message = ui.input("Message")
                ui.button("Publish", on_click=self.publish)

            ui.button("Start Periodic Publish", on_click=self.start_periodic_publish)
            ui.button("Stop Periodic Publish", on_click=self.stop_periodic_publish)

            self.message_area = ui.textarea(label="Received Messages", rows=10)

    def connect(self):
        # (keep the existing connect method)

    def disconnect(self):
        # ... (keep the existing disconnect method)

    def subscribe(self):
        # ... (keep the existing subscribe method)

    def publish(self):
        # ... (keep the existing publish method)

    def on_connect(self, client, userdata, flags, rc):
        # ... (keep the existing on_connect method)

    def on_message(self, client, userdata, msg):
        # ... (keep the existing on_message method)

    async def periodic_publish(self):
        if self.connected:
            message = f"Periodic message at {time.time()}"
            self.client.publish(self.publish_topic.value, message)
            ui.notify(f"Published periodic message to {self.publish_topic.value}", color="positive")

    def start_periodic_publish(self):
        if not self.connected:
            ui.notify("Please connect to a broker first", color="negative")
            return
        
        if not self.publish_topic.value:
            ui.notify("Please enter a publish topic", color="negative")
            return
        
        self.add_timed_event(30, self.periodic_publish)  # Publish every 30 seconds
        ui.notify("Periodic publish started")

    def stop_periodic_publish(self):
        self.stop_timed_events()
        ui.notify("Periodic publish stopped")

    def cleanup(self):
        super().cleanup()
        if self.connected:
            self.disconnect()
