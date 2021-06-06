import random
from collections import defaultdict
from datetime import datetime, timedelta
from time import sleep

from pynput import keyboard

controller = keyboard.Controller()

HOTKEY = "'`'"
MIN_DELAY = 0
MAX_DELAY = 50

MIN_PRESS_TIME = 50
MAX_PRESS_TIME = 150

# TODO: load from file
FLASK_DURATIONS = {
    "2": 3000,
    "3": 6000,
    "4": 9000,
    "5": 1000,
}

TIMEOUT_CACHE = defaultdict(lambda: datetime.now())


def use_flask(key: str):
    ends_at = TIMEOUT_CACHE[key] + timedelta(milliseconds=FLASK_DURATIONS[key])
    if ends_at < datetime.now():
        sleep(random.randint(MIN_DELAY, MAX_DELAY) / 1000)
        controller.press(key)
        sleep(random.randint(MIN_PRESS_TIME, MAX_PRESS_TIME) / 1000)
        controller.release(key)
        TIMEOUT_CACHE[key] = datetime.now()


def on_press(key):
    if str(key) == HOTKEY:
        for key in FLASK_DURATIONS.keys():
            use_flask(key)


def main():
    with keyboard.Listener(on_press=on_press) as listener:
        try:
            listener.join()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
