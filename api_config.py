import os

from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("ENV_API_BASE_URL")
