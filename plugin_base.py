# plugins/sample_plugin.py
from app import PluginBase
import logging

logger = logging.getLogger(__name__)

class Plugin(PluginBase):
    def __init__(self, app):
        super().__init__(app)
        logger.info("Sample plugin initialized")

    async def tick(self):
        logger.info("Sample plugin tick")