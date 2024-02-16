from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path
import moviepy.video.io.ImageSequenceClip
from time import sleep
import os


def create_folder(folder):
    os.makedirs(folder, exist_ok=True)


def get_device_pixel_ratio():
    options = Options()
    options.add_argument("--headless")
    service_object = Service(binary_path)
    driver = webdriver.Chrome(service=service_object, options=options)
    device_pixel_ratio = driver.execute_script(
        "return window.devicePixelRatio")
    driver.quit()
    return device_pixel_ratio


device_pixel_ratio = get_device_pixel_ratio()


class ScreenshotMaker:
    def __init__(self, url, width=1000, height=1000, sleep_interval=0.1, headless=True, crop_image=False):
        self.url = url
        self.width = width
        self.height = height
        self.screenshots = []
        self.sleep_interval = sleep_interval
        self.headless = headless
        self.crop_image = crop_image

    def __enter__(self):
        options = Options()
        if self.headless:
            options.add_argument("--headless")
        service_object = Service(binary_path)
        self.driver = webdriver.Chrome(
            service=service_object, options=options)
        if not self.headless:
            # put window in the dummy monitor
            self.driver.set_window_position(1500, 500)
        self.device_pixel_ratio = self.driver.execute_script(
            "return window.devicePixelRatio")
        self.driver.set_window_size(self.width, self.height)
        viewport_height = self.driver.execute_script(
            "return window.innerHeight")
        if viewport_height < self.height:
            self.driver.set_window_size(
                self.width, self.height + (self.height - viewport_height))
        viewport_height = self.driver.execute_script(
            "return window.innerHeight")
        if viewport_height < self.height:
            print(
                f"[warning] cannot set height to desired {self.height}, current height is {viewport_height}, please use a higher resolution")
        viewport_width = self.driver.execute_script("return window.innerWidth")
        if viewport_width < self.width:
            print(
                f"[warning] cannot set width to desired {self.width}, current width is {viewport_width}, please use a higher resolution")
        self.driver.get(self.url)
        self.driver.execute_script(f"hide_control()")
        return self

    def __exit__(self, *args):
        self.driver.quit()

    def make_screenshot(self, time, filepath, use_existing_images=False):
        if not use_existing_images:
            self.driver.execute_script(f"set_time({time})")
            sleep(self.sleep_interval)
            self.driver.get_screenshot_as_file(filepath)
            if self.crop_image:
                from PIL import Image
                im = Image.open(filepath)
                im1 = im.crop((0, 0, self.width, self.height))
                im1.save(filepath)
        self.screenshots.append(filepath)

    def make_video(self, fps, filepath):
        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(
            self.screenshots, fps=fps)
        clip.write_videofile(filepath)
