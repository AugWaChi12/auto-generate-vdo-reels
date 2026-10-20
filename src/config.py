import os
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"
ASSETS_DIR = ROOT_DIR / "assets"
BGM_DIR = ASSETS_DIR / "bgm"
OUTPUT_DIR = ROOT_DIR / "output"
DATABASE_FILE = ROOT_DIR / "tools_database.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
BGM_DIR.mkdir(parents=True, exist_ok=True)

# API Keys & Secrets
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
AFFILIATE_BIO_URL = os.getenv("AFFILIATE_BIO_URL", "https://top-ai-tools.bio")

# Video Settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FPS = 30

# Voice settings (Microsoft Edge-TTS Free Voices)
# Options: en-US-ChristopherNeural, en-US-GuyNeural, en-US-JennyNeural, en-GB-RyanNeural
VOICE_NAME = os.getenv("VOICE_NAME", "en-US-ChristopherNeural")
VOICE_RATE = "+5%"
VOICE_PITCH = "+0Hz"

# Audio Settings
BGM_VOLUME = 0.12  # Subtle background music volume
VOICE_VOLUME = 1.0

# Gemini Model
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
