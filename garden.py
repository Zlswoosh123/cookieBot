from clicker import Clicker
import os
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
from selenium.common.exceptions import StaleElementReferenceException, ElementNotInteractableException
import traceback

class Garden():
    def __init__(self, clicker):
        print(f"Clicker type is: {type(clicker)}")
        self.driver = clicker.driver
        self.action = clicker.action


    def proper_click(self, ele):
        try:
            self.action.move_to_element(ele).click().perform()
        except StaleElementReferenceException:
            print("Whoops element expired!")
            pass
        except:
            traceback.print_exc()

    def proper_wait(self, css_select):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"{css_select}")))

    def garden_start(self):
        print("Garden starting!")
        self.garden_button = self.driver.find_element(By.CSS_SELECTOR, "#productMinigameButton2")
        print("Printing garden texts")
        print(self.garden_button.text)
        if self.garden_button.text == "Close Garden":
            print("Skipped opening garden, already open")
        else:
            self.action.move_to_element(self.garden_button)
            self.proper_click(self.garden_button)
            print("Clicked garden button")
        self.proper_wait("#gardenTool-1")
        self.harvest = self.driver.find_element(By.CSS_SELECTOR,"#gardenTool-1")
        self.proper_click(self.harvest)
        print("Harvested seeds")


    def get_tiles(self):
        print("get_tiles starting!")
        self.tile_list = []
        all_tiles = self.driver.find_elements(By.CSS_SELECTOR, ".gardenTile")
        self.garden_tile = all_tiles[0].get_attribute("style")
        for tile in all_tiles:
            text = tile.get_attribute("style")
            if "display: block" in text:
                self.tile_list.append(tile)
                # self.tile_list.append(tile.get_attribute("id"))

        print(len(self.tile_list))
        return self.tile_list

    def add_seed(self,tile_list: list):
        print("add_Seed starting!")
        seed_count = 0
        for tile in tile_list:
            try:
                print(f"Working on seed {seed_count}")
                self.seed = self.driver.find_element(By.CSS_SELECTOR, "#gardenSeed-1")
                print("Clicking seed on plot")
                self.action.click(self.seed).pause(.1).move_to_element_with_offset(tile, 0, 12).pause(.1).click().perform()
            except ElementNotInteractableException:
                pass
            except:
                traceback.print_exc()
            else:
                seed_count += 1
