import os

from dotenv import load_dotenv

load_dotenv()

TMDB_BEARER_TOKEN = os.getenv("ENV_TMDB_BEARER_TOKEN")
