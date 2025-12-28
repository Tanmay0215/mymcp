"""
Configuration and environment variable management.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_gmail_config():
    """Get Gmail SMTP configuration from environment variables."""
    return {
        "user": os.getenv("GMAIL_USER"),
        "password": os.getenv("GMAIL_APP_PASSWORD"),
        "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        "smtp_port": int(os.getenv("SMTP_PORT", "587"))
    }
