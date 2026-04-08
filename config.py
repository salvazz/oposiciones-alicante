import os
from datetime import timedelta

class Config:
    """Application configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Email settings
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'tu-email@gmail.com')
    SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', 'tu-password')

    # Recipients
    RECIPIENT_EMAILS_STR = os.getenv('RECIPIENT_EMAILS', 'salvazz@gmail.com,lucasaliagadelaencarnacion@gmail.com')
    RECIPIENT_EMAILS = [email.strip() for email in RECIPIENT_EMAILS_STR.split(',')]

    # Scraping settings
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '10'))
    CACHE_DURATION = int(os.getenv('CACHE_DURATION', '3600'))  # 1 hour

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # Development settings
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    TESTING = os.getenv('FLASK_TESTING', 'False').lower() == 'true'