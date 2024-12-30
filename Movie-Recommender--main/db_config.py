import os

from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("ENV_MYSQL_HOST")
USER = os.getenv("ENV_MYSQL_USER")
PASSWORD = os.getenv("ENV_MYSQL_PASSWORD")
