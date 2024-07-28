from applogger import plugin_logger

# Plugin base class
class PluginBase:
    def __init__(self, app):
        self.app = app
        self.enabled = True

    async def tick(self):
        pass

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True