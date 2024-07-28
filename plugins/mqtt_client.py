# plugins/mqtt_plugin.py
from plugin_base import PluginBase
from applogger import plugin_logger
import paho.mqtt.client as mqtt
class Plugin(PluginBase):
    def __init__(self, app):
        super().__init__(app)
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("openhab", 1883, 60)  # Replace with your MQTT broker
        self.client.loop_start()
        plugin_logger.info("MQTT plugin initialized")

    def on_connect(self, client, userdata, flags, rc):
        plugin_logger.info(f"Connected with result code {rc}")
        self.client.subscribe("test/topic")  # Replace with your topic

    def on_message(self, client, userdata, msg):
        plugin_logger.info(f"{msg.topic} {str(msg.payload)}")

    async def tick(self):
        # Perform periodic MQTT operations here if needed
        self.client.subscribe("test/tick")  # Replace with your topic
        plugin_logger.info("MQTT plugin tick")
        pass

    def publish_message(self, topic, message):
        self.client.publish(topic, message)
        plugin_logger.info(f"Published message to {topic}: {message}")

    def __del__(self):
        self.client.loop_stop()