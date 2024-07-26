from abc import ABC, abstractmethod
from nicegui import ui
import asyncio
from logger_config import plugin_logger

class PluginBase(ABC):
    def __init__(self):
        self.timed_events = []

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    def add_timed_event(self, interval, callback):
        """
        Add a timed event to the plugin.
        :param interval: Time interval in seconds
        :param callback: Function to be called at each interval
        """
        async def timed_task():
            while True:
                try:
                    await asyncio.sleep(interval)
                    await callback()
                except Exception as e:
                    plugin_logger.error(f"Error in timed event for {self.name}: {str(e)}")

        task = asyncio.create_task(timed_task())
        self.timed_events.append(task)
        plugin_logger.info(f"Added timed event for {self.name} with interval {interval}s")

    def stop_timed_events(self):
        for task in self.timed_events:
            task.cancel()
        self.timed_events.clear()
        plugin_logger.info(f"Stopped all timed events for {self.name}")

    def cleanup(self):
        self.stop_timed_events()
        plugin_logger.info(f"Cleaned up {self.name}")
