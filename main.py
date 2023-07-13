import os
import random
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import keyboard
import glob
import re
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import clicker
from random import choice
import traceback
from garden import Garden

chrome_driver_path = "C:\Development\chromedriver.exe"  # https://chromedriver.chromium.org/downloads

# start clicker
clicker = clicker.Clicker()
clicker.startup()  # go through init screens and load latest file
# set vars from clicker
driver = clicker.driver
cookie = clicker.cookie
pause = clicker.pause
garden = Garden(clicker)
wait_period = clicker.wait_period
wait_list = [30]
# wait_list = [900, 2400, 3600, 5400]

# timeouts
timeout = time.time() + wait_period  # main timeout used for init buying logic
program_timeout = time.time() + 60 * 60 * 24 * 30 * 12  # ~1 year
save_timeout = time.time() + 3600  # save every hour
print_timeout = time.time() + 60  # Prints time until main timeout
elder_timeout = time.time() + 5  # clicks elder pledge
garden_timeout = time.time() + 1800  # runs garden minigame

print(f"startup timeout is: {timeout - time.time()}")
# Close opening screens
try:
    if EC.presence_of_element_located((By.CSS_SELECTOR, ".cc_btn")):
        driver.find_element(by="css selector", value=".cc_btn").click()
except NoSuchElementException:
    pass

# Close opening screens
try:
    if EC.presence_of_element_located((By.CSS_SELECTOR, "#note-1 .close")):
        try:
            driver.find_element(by="css selector", value="#note-1 .close").click()
        except StaleElementReferenceException:
            print("Stale element on pre-start, skipping")
except NoSuchElementException:
    pass

clicker.find_tech()  # buys tech right away, not actually needed

# Main Loop
while True:
    clicker.gc = clicker.driver.find_elements(by="css selector", value=".shimmer")  # finds golden cookies to click
    while len(clicker.gc) > 0:  # if a golden cookie is found, click it
        print(f"{EC.element_to_be_clickable((By.CSS_SELECTOR, '.shimmer'))}")
        try:
            clicker.golden_cookie_check()
        except:
            traceback.print_exc()
            break

    clicker.main_click()  # does most of the clicking

    # Admin mode control, see README for details
    if keyboard.is_pressed("home"):
        clicker.stop_func()
        if clicker.user_input == "garden":
            clicker.close_menus()
            garden.garden_start()
            garden.add_seed(garden.get_tiles())
            garden_timeout = time.time() + (60 * 75)
        elif clicker.user_input == "wait":
            timeout = time.time() + clicker.wait_period
        elif clicker.user_input == "elder":
            elder_timeout = time.time() + 1810
        else:
            print("stop ended")
            continue
        print("stop ended")

    # plants seeds in the garden
    if time.time() > garden_timeout:
        clicker.close_menus()
        try:
            garden.garden_start()
            garden.add_seed(garden.get_tiles())
        except:
            traceback.print_exc()
        finally:
            garden_timeout = time.time() + (60 * 75)

    # main timeout sequence to buy stuff
    if time.time() > timeout:
        clicker.timeout_sequence()
        timeout = time.time() + clicker.wait_period
        clicker.close_menus()
        print(f"program timeout in: {program_timeout - time.time()}")
        print(f"new timeout is: {timeout - time.time()}")

    # prints timeout every 60s
    if time.time() > print_timeout:
        print(f"New timeout set! It is: {timeout - time.time()}")
        print_timeout = time.time() + 60
    # clicks elder pledge
    if time.time() > elder_timeout:
        clicker.elder_pledge()
        elder_timeout = time.time() + (1810)

    # run save to file logic
    if time.time() > save_timeout:
        time.sleep(1)
        print("trying to save file...")
        try:
            clicker.save_file()
        except:
            print("WARNING save not completed, check for error")
            traceback.print_exc()
        finally:
            save_timeout = time.time() + 1800
            clicker.close_menus()

    # Close the program after a long time
    if time.time() > program_timeout:
        clicker.save_file()
        cookie_per_s = driver.find_element(by="id", value="cookies").text
        print(cookie_per_s)
        break
