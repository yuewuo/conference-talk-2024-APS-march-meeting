import common
import os
import time
from alive_progress import alive_bar

NAME = "triangle_color_code_example"

FOLDER = f"screenshots_{NAME}"
common.create_folder(FOLDER)

WIDTH = 4400
HEIGHT = 1400
URL = f"http://localhost:8099/index.html?animation={NAME}"
FRAME_RATE = 60
# FRAME_RATE = 5  # for debugging
DURATION = 45

USE_EXISTING_IMAGES = False
if 'USE_EXISTING_IMAGES' in os.environ and os.environ["USE_EXISTING_IMAGES"] != "":
    USE_EXISTING_IMAGES = True

"""
need a large-enough monitor (at least 4400 * 2000) to take the video, because headless mode doesn't work somehow
On macOS, you can use https://github.com/waydabber/BetterDisplay to add dummy display and mirror it to your main display
"""

with common.ScreenshotMaker(URL, WIDTH, HEIGHT, sleep_interval=0.5, headless=False) as maker:
    count = int(DURATION * FRAME_RATE + 1)
    time.sleep(5)  # loading three.js
    with alive_bar(count) as bar:
        for frame in range(count):
            maker.make_screenshot(
                frame / FRAME_RATE, f"{FOLDER}/{frame}.png", use_existing_images=USE_EXISTING_IMAGES)
            bar()
    maker.make_video(FRAME_RATE, f"{NAME}.mp4")
