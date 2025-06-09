import json
from pathlib import Path

DEFAULT_CONFIG = {
    "grid_size": [50, 30],
    "cell_size": 20,
    "speed": 10,
    "theme": "light"
}

CONFIG_PATH = Path(__file__).parent / ".game_of_life_config.json"


def load_settings() -> dict:
    """
    Wczytuje ustawienia z pliku JSON.

    Jeśli plik nie istnieje, tworzy go z domyślnymi wartościami.

    :return: słownik ustawień
    :rtype: dict
    """
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)
        for key, val in DEFAULT_CONFIG.items():
            if key not in data:
                data[key] = val
        return data
    else:
        save_settings(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()


def save_settings(settings: dict):
    """
    Zapisuje przekazane ustawienia do pliku JSON.

    :param settings: słownik ustawień do zapisania
    :type settings: dict
    """
    with open(CONFIG_PATH, "w") as f:
        json.dump(settings, f, indent=4)