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

BRANCH_OFFSET = 33.5
LEFT_ARROW = 'left'
RIGHT_ARROW = 'right'


LEFT_BRANCH = {
    'x': 307,
    'y': int(468 + BRANCH_OFFSET),
    'color': (161, 116, 56),
}

RIGHT_BRANCH = {
    'x': 382,
    'y': int(468 + BRANCH_OFFSET),
    'color': (161, 116, 56),
}

RELOAD_POSITION = {
    'x': 345,
    'y': 662,
    'color': (198, 151, 91),
}


def pixelMatchesColor(x, y, color=()):
    img = sct.grab(monitor)
    return img.pixel(x, y) == color


def playable():
    return pixelMatchesColor(
        RELOAD_POSITION['x'],
        RELOAD_POSITION['y'],
        (255, 255, 255)
    )


def orchestrator():
    # wait for animation
    sleep(.15)

    image = sct.grab(monitor)

    coords = []

    for index in range(12):
        left_arrow_y = int(LEFT_BRANCH['y'] - (index * BRANCH_OFFSET))
        right_arrow_y = int(RIGHT_BRANCH['y'] - (index * BRANCH_OFFSET))

        coords.append(
            (
                image.pixel(LEFT_BRANCH['x'],
                            left_arrow_y) == LEFT_BRANCH['color'],
                image.pixel(RIGHT_BRANCH['x'],
                            right_arrow_y) == RIGHT_BRANCH['color']
            )
        )

    return coords


sleep(3)

while True:
    last_choice = LEFT_ARROW
    coords = orchestrator()

    for c in coords:
        c = map(lambda x: 'BRANCH' if x else 'FREE', c)
        print(list(c))

    for coord_index in range(len(coords) - 1):
        current_positon_left_branch, current_positon_right_branch = coords[coord_index]
        next_positon_left_branch, next_positon_right_branch = coords[coord_index + 1]

        print(current_positon_left_branch, current_positon_right_branch)
        print(next_positon_left_branch, next_positon_right_branch)

        # ['FREE', 'FREE']
        # ['FREE', 'FREE']
        if not current_positon_left_branch and not current_positon_right_branch and \
                not next_positon_left_branch and not next_positon_right_branch:
            pyautogui.press(LEFT_ARROW)

        # ['BRANCH', 'FREE']
        # ['FREE', 'FREE']
        if current_positon_left_branch and not current_positon_right_branch and \
                not next_positon_left_branch and not next_positon_right_branch:
            pyautogui.press(RIGHT_ARROW)

        # ['FREE', 'FREE']
        # ['BRANCH', 'FREE']
        if not current_positon_left_branch and not current_positon_right_branch and \
                next_positon_left_branch and not next_positon_right_branch:
            pyautogui.press(RIGHT_ARROW)

        # ['FREE', 'BRANCH']
        # ['FREE', 'FREE']
        if not current_positon_left_branch and current_positon_right_branch and \
                not next_positon_left_branch and not next_positon_right_branch:
            pyautogui.press(LEFT_ARROW)

        # ['FREE', 'FREE']
        # ['FREE', 'BRANCH']
        if (not current_positon_left_branch and not current_positon_right_branch and \
                not next_positon_left_branch and next_positon_right_branch):
            pyautogui.press(LEFT_ARROW)
