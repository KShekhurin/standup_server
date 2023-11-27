from dotenv import load_dotenv
import os

# .env should be in one foulder with settings.py
load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
