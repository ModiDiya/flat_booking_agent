import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Base project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Google credentials file path
GOOGLE_CREDENTIALS_FILE = os.getenv(
    "GOOGLE_CREDENTIALS_FILE",
    os.path.join(BASE_DIR, "credentials.json")
)

# Email settings for confirmation
EMAIL_SENDER = os.getenv("EMAIL_SENDER")      # your email address
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # app password if Gmail
