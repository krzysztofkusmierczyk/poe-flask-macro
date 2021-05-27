import random
from collections import defaultdict
from datetime import datetime, timedelta
from time import sleep

from pynput import keyboard

controller = keyboard.Controller()

MIN_DELAY = 0
MAX_DELAY = 150

FLASK_DURATIONS = {
    '2': 3000,
    '3': 6000,
    '4': 9000,
    '5': 1000,
}

TIMEOUT_CACHE = defaultdict(lambda: datetime.now())


def use_flask(key: str):
    if TIMEOUT_CACHE[key] + timedelta(milliseconds=FLASK_DURATIONS[key]) < datetime.now():
        sleep(random.randint(MIN_DELAY, MAX_DELAY)/1000)
        controller.press(key)
        TIMEOUT_CACHE[key] = datetime.now()


def on_press(key):
    if str(key) == "'`'":
        for key in FLASK_DURATIONS.keys():
            use_flask(key)


def main():
    with keyboard.Listener(
            on_press=on_press) as listener:
        try:
            listener.join()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()