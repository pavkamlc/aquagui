from nicegui import ui, app
import sqlite3
import bcrypt
import importlib
import os
import RPi.GPIO as GPIO
from plugin_base import PluginBase
from logger_config import main_logger, plugin_logger

# Use main_logger instead of print statements
main_logger.info("Application started")

# Database setup
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT,
        is_admin BOOLEAN
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS config (
        key TEXT PRIMARY KEY,
        value TEXT
    )
''')

conn.commit()

# User management
def register_user(username, password, is_admin=False):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)", (username, hashed, is_admin))
    conn.commit()
    main_logger.info(f"User registered: {username}")

def validate_user(username, password):
    cursor.execute("SELECT password, is_admin FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result:
        is_valid = bcrypt.checkpw(password.encode('utf-8'), result[0])
        main_logger.info(f"User login attempt: {username}, Success: {is_valid}")
        return is_valid, result[1]
    main_logger.warning(f"Login attempt for non-existent user: {username}")
    return False, False

# Configuration management
def set_config(key, value):
    cursor.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", (key, value))
    conn.commit()

def get_config(key):
    cursor.execute("SELECT value FROM config WHERE key = ?", (key,))
    result = cursor.fetchone()
    return result[0] if result else None

# Plugin management
plugins = {}

def load_plugins():
    plugin_dir = 'plugins'
    for filename in os.listdir(plugin_dir):
        if filename.endswith('.py'):
            module_name = filename[:-3]
            try:
                module = importlib.import_module(f'{plugin_dir}.{module_name}')
                if hasattr(module, 'setup'):
                    plugin = module.setup()
                    if isinstance(plugin, PluginBase):
                        plugins[plugin.name] = plugin
                        plugin_logger.info(f"Loaded plugin: {plugin.name}")
                    else:
                        plugin_logger.warning(f"Invalid plugin type: {module_name}")
            except Exception as e:
                plugin_logger.error(f"Error loading plugin {module_name}: {str(e)}")

# Main app
@ui.page('/')
def main_page():
    ui.label('Welcome to the NiceGUI App')
    
    with ui.row():
        username = ui.input('Username')
        password = ui.input('Password', password=True)
        ui.button('Login', on_click=lambda: login(username.value, password.value))
        ui.button('Register', on_click=lambda: register(username.value, password.value))

    # Plugin section
    with ui.column():
        ui.label('Plugins')
        for plugin_name, plugin in plugins.items():
            ui.button(plugin_name, on_click=lambda p=plugin: p.run())

def login(username, password):
    is_valid, is_admin = validate_user(username, password)
    if is_valid:
        ui.notify('Login successful')
        main_logger.info(f"User logged in: {username}")
        if is_admin:
            ui.notify('Logged in as admin')
            main_logger.info(f"Admin logged in: {username}")
    else:
        ui.notify('Invalid username or password', color='negative')
        main_logger.warning(f"Failed login attempt: {username}")

def register(username, password):
    try:
        register_user(username, password)
        ui.notify('Registration successful')
        main_logger.info(f"New user registered: {username}")
    except sqlite3.IntegrityError:
        ui.notify('Username already exists', color='negative')
        main_logger.warning(f"Registration attempt with existing username: {username}")

def create_admin_if_not_exists():
    cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1")
    if cursor.fetchone()[0] == 0:
        admin_password = 'admin'  # You should change this to a secure password
        register_user('admin', admin_password, is_admin=True)
        main_logger.info("Initial admin user created. Username: admin, Password: admin")
        main_logger.warning("Please change the admin password after first login.")

# Cleanup function
def cleanup():
    for plugin in plugins.values():
        try:
            plugin.cleanup()
            plugin_logger.info(f"Cleaned up plugin: {plugin.name}")
        except Exception as e:
            plugin_logger.error(f"Error cleaning up plugin {plugin.name}: {str(e)}")
    main_logger.info("Application shutting down")

# Create initial admin user
create_admin_if_not_exists()

# Load plugins
load_plugins()

#PM
app.on_shutdown(cleanup)

# Run the app
main_logger.info("Starting NiceGUI application")
ui.run(title='NiceGUI App')
