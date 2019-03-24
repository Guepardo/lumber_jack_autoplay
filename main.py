import pyautogui
import mss

from IPython import embed
from time import sleep
from datetime import datetime
mon = {"top": 0, "left": 0, "width": 100, "height": 100}

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
    mon['top'] = y - 1
    mon['left'] = x - 1
    img = sct.grab(mon)
    mss.tools.to_png(img.rgb, img.size, output="nada.png")
    return img.pixel(5, 0) == color


def playable():
    return pixelMatchesColor(
        RELOAD_POSITION['x'],
        RELOAD_POSITION['y'],
        (255, 255, 255)
    )


def orchestrator(last_choice=(LEFT_ARROW['x'], LEFT_ARROW['y'])):
    has_left_branch = pixelMatchesColor(
        LEFT_BRANCH['x'],
        LEFT_BRANCH['y'],
        LEFT_BRANCH['color']
    )

    if has_left_branch:
        print('RIGHT')
        return (RIGHT_ARROW['x'], RIGHT_ARROW['y'])

    has_right_branch = pixelMatchesColor(
        RIGHT_BRANCH['x'],
        RIGHT_BRANCH['y'],
        RIGHT_BRANCH['color']
    )

    if has_right_branch:
        print('LEFT')
        return (LEFT_ARROW['x'], LEFT_ARROW['y'])

    if not has_left_branch and not has_right_branch:
        print('LAST CHOICE')
        return last_choice


sleep(3)

last_orchestrator_choice = (LEFT_ARROW['x'], LEFT_ARROW['y'])

count = 0

while True:
    print(datetime.now())
    x, y = orchestrator(last_orchestrator_choice)

    sleep(0.5)
    pyautogui.click(x, y)
    print(datetime.now())

    last_orchestrator_choice = (x, y)

    # if count % 10 == 0: 
    #     if not playable(): 
    #         break