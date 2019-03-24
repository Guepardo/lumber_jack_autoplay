import pyautogui
import mss

from IPython import embed
from time import sleep
from datetime import datetime
mon = {"top": 0, "left": 0, "width": 800, "height": 900}

LEFT_BRANCH = {
    'x': 342,
    'y': 465,
    'color': (161, 116, 56),
}

RIGHT_BRANCH = {
    'x': 457,
    'y': 465,
    'color': (161, 116, 56),
}

LEFT_ARROW = {
    'x': 318,
    'y': 755,
    'color': (161, 116, 56),
}

RIGHT_ARROW = {
    'x': 481,
    'y': 755,
    'color': (161, 116, 56),
}

RELOAD_POSITION = {
    'x': 394,
    'y': 755,
    'color': (198, 151, 91),
}

sct = mss.mss()


def pixelMatchesColor(x, y, color=()):
    img = sct.grab(mon)
    return img.pixel(x, y) == color


def playable():
    return pixelMatchesColor(
        RELOAD_POSITION['x'],
        RELOAD_POSITION['y'],
        (255, 255, 255)
    )


def orchestrator():
    sleep(3)
    img = sct.grab(mon)

    coords = []

    for index in range(4):
        coords.append(
            (
                img.pixel(LEFT_BRANCH['x'], LEFT_BRANCH['y'] -
                          (index * 100)) == LEFT_BRANCH['color'],
                img.pixel(RIGHT_BRANCH['x'], RIGHT_BRANCH['y'] -
                          (index * 100)) == RIGHT_BRANCH['color']
            )
        )

    return coords


sleep(3)
count = 0

pyautogui.click(LEFT_ARROW['x'], LEFT_ARROW['y'])
sleep(1)

while True:
    coords = orchestrator()

    for c in coords: 
        print(c)

    sleep(10)
    for (has_left_branch, has_right_branch) in coords:
        count += 1

        if count % 5 == 0:
            if not playable():
                break

        print()
        if has_left_branch:
            print(has_left_branch, has_right_branch, '-- right')
            pyautogui.click(RIGHT_ARROW['x'], RIGHT_ARROW['y'])
            continue

        if has_right_branch:
            print(has_left_branch, has_right_branch, '-- left')
            pyautogui.click(LEFT_ARROW['x'], LEFT_ARROW['y'])
            continue

        print(has_left_branch, has_right_branch, '-- left [auto]')
        pyautogui.click(LEFT_ARROW['x'], LEFT_ARROW['y'])
