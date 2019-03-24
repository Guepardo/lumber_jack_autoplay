import pyautogui
import mss

from IPython import embed
from time import sleep
from datetime import datetime

# Monitor specifications

monitor = {
    "top": 0,
    "left": 0,
    "width": 683,
    "height": 767
}

# MSS global instance

sct = mss.mss()


# Constants

LEFT_BRANCH = {
    'x': 286,
    'y': 334,
    'color': (161, 116, 56),
}

RIGHT_BRANCH = {
    'x': 400,
    'y': 333,
    'color': (161, 116, 56),
}

LEFT_ARROW = 'left'
RIGHT_ARROW = 'right'

RELOAD_POSITION = {
    'x': 339,
    'y': 627,
    'color': (198, 151, 91),
}


def pixelMatchesColor(x, y, color=(), image=None):
    if not image:
        image = sct.grab(monitor)

    mss.tools.to_png(image.rgb, image.size, output="nada.png")

    print(image.pixel(x, y))

    return image.pixel(x, y) == color


def playable():
    return pixelMatchesColor(
        RELOAD_POSITION['x'],
        RELOAD_POSITION['y'],
        (255, 255, 255)
    )


def orchestrator(last_choice=LEFT_ARROW):
    image = sct.grab(monitor)

    has_left_branch = pixelMatchesColor(
        LEFT_BRANCH['x'],
        LEFT_BRANCH['y'],
        LEFT_BRANCH['color'],
        image
    )

    if has_left_branch:
        print('RIGHT')
        return RIGHT_ARROW

    has_right_branch = pixelMatchesColor(
        RIGHT_BRANCH['x'],
        RIGHT_BRANCH['y'],
        RIGHT_BRANCH['color'],
        image
    )

    if has_right_branch:
        print('LEFT')
        return LEFT_ARROW

    return last_choice


sleep(3)

last_orchestrator_choice = LEFT_ARROW

count = 0

while True:
    command = orchestrator(last_orchestrator_choice)

    sleep(0.1)

    pyautogui.press(command)

    last_orchestrator_choice = command

    if count % 10 == 0:
        if not playable():
            break

    count += 1
