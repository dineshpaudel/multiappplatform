import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# Platform Settings
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.path.join('logs', 'app.log')

# API Models
API_PROVIDERS = {
    "OpenAI": {
        "models": ["gpt-3.5-turbo-0125", "gpt-4o-mini"]
    },
    "DeepSeek": {
        "models": ["deepseek-chat", "deepseek-coder"]
    },
    "Gemini": {
        "models": ["gemini-pro", "gemini-1.5-pro", "gemini-1.5-flash"]
    }
}

# Default temperature for AI model responses
DEFAULT_TEMPERATURE = 0.7

# TTS Settings
TTS_VOICES = [
    {
        "name": "en-US-Standard-F",
        "display_name": "Female Voice",
        "gender": "FEMALE"
    },
    {
        "name": "en-US-Standard-I",
        "display_name": "Male Voice",
        "gender": "MALE"
    }
]

TTS_SPEEDS = [
    {"value": 1.0, "display": "Normal"},
    {"value": 0.75, "display": "Slow"},
    {"value": 1.25, "display": "Fast"}
]