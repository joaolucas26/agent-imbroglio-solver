import os
import json
from typing import Any
from google import genai


def load_config():
    """Loads the main configuration from the root directory."""
    config_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "config.json")
    )
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_client() -> Any:

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=GEMINI_API_KEY)

    return client
