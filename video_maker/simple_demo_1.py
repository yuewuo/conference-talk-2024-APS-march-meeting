import common
import time

VUE_FILE = "simple_demo"
NAME = f"{VUE_FILE}_1"

WIDTH = 4400
HEIGHT = 2000
URL = f"http://localhost:8099/index.html?animation={VUE_FILE}"

"""
need a large-enough monitor (at least 4400 * 2000) to take the video, because headless mode doesn't work somehow
On macOS, you can use https://github.com/waydabber/BetterDisplay to add dummy display and mirror it to your main display
"""

with common.ScreenshotMaker(URL, WIDTH, HEIGHT, sleep_interval=0.5, headless=False) as maker:
    time.sleep(5)  # loading three.js
    maker.make_screenshot(0, f"{NAME}.png")
