"""
This module contains all the settings required
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project directories
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
REPORT_DIR = os.path.join(PROJECT_DIR, 'reports')
SCREENSHOT_PATH = os.path.join(REPORT_DIR, 'evidences')

# Ensure directories exist
os.makedirs(SCREENSHOT_PATH, exist_ok=True)

# Application settings
BASE_URL = os.getenv("BASE_URL", "https://m.twitch.tv/")

# Browser configuration
SUPPORTED_BROWSERS = ['Chrome', 'Edge']
DEFAULT_BROWSER = os.getenv("BROWSER", "Chrome")

# Timeout configuration (in seconds)
DEFAULT_WAIT_TIMEOUT = int(os.getenv("DEFAULT_WAIT_TIMEOUT", "5"))

# Headless mode
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
