"""Konfigurace prostředí a cesty k datům."""

import os
from pathlib import Path
from dotenv import load_dotenv


# Načtení .env souboru
load_dotenv()


class Config:
    """Nastavení konfigurace pro práci s cestami."""

    # Základní nastavení
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Web scraping
    BASE_URL = "https://dataglossary.wyscout.com/"
    USER_AGENT = os.getenv(
        "USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    REQUEST_DELAY = float(os.getenv("REQUEST_DELAY", "1"))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    TIMEOUT = int(os.getenv("TIMEOUT", "30"))

    # Cesty
    BASE_DIR = Path(__file__).parent
    OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "./output"))
    IMAGES_DIR = Path(os.getenv("IMAGES_DIR", "./data/raw/images"))
    LOGS_DIR = Path("./logs")

    # Vytvoření složek
    OUTPUT_DIR.mkdir(exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)

    # API keys (pokud budete potřebovat)
    WYSCOUT_API_KEY = os.getenv("WYSCOUT_API_KEY")

    # Email nastavení
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


# Singleton instance
config = Config()
