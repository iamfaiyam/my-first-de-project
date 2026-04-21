import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.cricapi.com/v1"
API_KEY = "9fc45154-1dd7-4a1d-adf2-fd8297f0d9ca"


def fetch_matches(offset: int = 0) -> dict:
    """
    Fetch match list data from CricAPI.
    Docs/sample format uses:
    /v1/matches?apikey=...&offset=0
    """
    if not API_KEY:
        raise ValueError("CRICAPI_KEY not found in environment variables.")

    url = f"{BASE_URL}/matches"
    params = {
        "apikey": API_KEY,
        "offset": offset
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def save_raw_data(data: dict, filepath: str) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
