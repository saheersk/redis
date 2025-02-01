import json
import os
from typing import Dict, Any

PERSISTENCE_FILE = "redis_data.json"


class DataStore:
    _instance = None
    _data: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.load_data()
        return cls._instance

    def load_data(self):
        if os.path.exists(PERSISTENCE_FILE):
            with open(PERSISTENCE_FILE, "r") as f:
                self._data = json.load(f)

    def save_data(self):
        with open(PERSISTENCE_FILE, "w") as f:
            json.dump(self._data, f)
        print(f"Data saved to {PERSISTENCE_FILE}")
