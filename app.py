# app.py
import asyncio
from nicegui import ui, app
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from logger_config import main_logger, plugin_logger
from datetime import datetime
import importlib
import os

# Set up logging
#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Database setup
Base = declarative_base()
engine = create_engine('sqlite:///app.db')
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

class Config(Base):
    __tablename__ = 'config'
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(String)

Base.metadata.create_all(engine)

# App class
class NiceGUIApp:
    def __init__(self):
        self.plugins = []
        self.load_plugins()
        self.setup_database()
        self.setup_ui()

    def load_plugins(self):
        plugin_dir = 'plugins'
        for filename in os.listdir(plugin_dir):
            if filename.endswith('.py') and filename != '__init__.py':
                module_name = f'plugins.{filename[:-3]}'
                module = importlib.import_module(module_name)
                plugin_class = getattr(module, 'Plugin')
                self.plugins.append(plugin_class(self))
        main_logger.info(f"Loaded {len(self.plugins)} plugins")

    def setup_database(self):
        with Session() as session:
            admin = session.query(User).filter_by(username='admin').first()
            if not admin:
                admin = User(username='admin', password='admin', is_admin=True)
                session.add(admin)
                session.commit()
                logger.info("Created default admin user")

    def setup_ui(self):
        @ui.page('/')
        def index():
            ui.label('Welcome to the NiceGUI App')
            self.time_label = ui.label()
            ui.timer(1, self.update_time)

    def update_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.set_text(f"Current time: {current_time}")

    async def run_plugins(self):
        while True:
            for plugin in self.plugins:
                if plugin.enabled:
                    await plugin.tick()
            await asyncio.sleep(1)

# Initialize and run the app
nice_gui_app = NiceGUIApp()

@app.on_startup
async def startup():
    asyncio.create_task(nice_gui_app.run_plugins())

ui.run()