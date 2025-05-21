# Модуль для работы с файлами сохранений. 
# Здесь реализованы функции сохранения и загрузки состояния игры 
# в формате JSON. Позволяет продолжить игру
#  с последнего сохранения.
import json
import os

SAVE_FILE = "savegame.json"

def save_game(session, filename="savegame.json"):
    state = {
        "player": {
            "health": session.player.current_health,
            "treasure": session.player.treasure_value,
            "position": session.player.get_position(),
            "move_count": session.player.move_count,
            "enemies_killed": session.player.enemies_killed,
            "food_eaten": session.player.food_eaten,
            "potions_drunk": session.player.potions_drunk,
            "scrolls_read": session.player.scrolls_read,
            "hits_delivered": session.player.hits_delivered,
            "hits_received": session.player.hits_received
        },
        "current_level": session.current_level
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4)

def load_game(filename="savegame.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            state = json.load(f)
        return state
    except FileNotFoundError:
        return None

def _empty_state() -> dict:
    return {"in_progress": None, "attempts": []}


def _read() -> dict:
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return _empty_state()


def _write(state: dict):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4)

def load_attempts() -> list:
    return _read().get("attempts", [])


def save_attempts(attempts: list):
    st = _read()
    st["attempts"] = attempts
    _write(st)


def load_in_progress() -> dict | None:
    return _read().get("in_progress")


def save_in_progress(progress: dict | None):
    st = _read()
    st["in_progress"] = progress
    _write(st)
