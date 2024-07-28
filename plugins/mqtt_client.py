# plugins/mqtt_plugin.py
from app import PluginBase
import logging
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

class Plugin(PluginBase):
    def __init__(self, app):
        super().__init__(app)
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("mqtt.eclipse.org", 1883, 60)  # Replace with your MQTT broker
        self.client.loop_start()
        logger.info("MQTT plugin initialized")

    def on_connect(self, client, userdata, flags, rc):
        logger.info(f"Connected with result code {rc}")
        client.subscribe("test/topic")  # Replace with your topic

    def on_message(self, client, userdata, msg):
        logger.info(f"{msg.topic} {str(msg.payload)}")

    async def tick(self):
        # Perform periodic MQTT operations here if needed
        pass

    def publish_message(self, topic, message):
        self.client.publish(topic, message)
        logger.info(f"Published message to {topic}: {message}")

    def __del__(self):
        self.client.loop_stop()