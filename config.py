import sys
from pathlib import Path

# Paths configuration for Twitter Shill Bot
BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"
ACCOUNTS_FILE = BASE_DIR / "accounts.json"
COOKIES_FILE = BASE_DIR / "cookies.json"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
