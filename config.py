import os
from dotenv import load_dotenv

load_dotenv()

# Football Data API

FOOTBALL_DATA_API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")

BASE_URL = "https://api.football-data.org/v4"

HEADERS = {
    "X-Auth-Token": FOOTBALL_DATA_API_KEY
}

# Gemini

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")