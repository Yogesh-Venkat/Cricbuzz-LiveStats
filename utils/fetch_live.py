import os
import requests

def fetch_live_matches(api_key=None, timeout=10):
    key = api_key or os.getenv("CRICBUZZ_API_KEY")
    if not key:
        return None
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None

def fetch_scorecard(match_id, api_key=None, timeout=10):
    key = api_key or os.getenv("CRICBUZZ_API_KEY")
    if not key:
        return None
    url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{match_id}/scard"
    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None
