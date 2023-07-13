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



class Clicker():
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get("https://orteil.dashnet.org/cookieclicker/")
        self.pause = False
        self.wait_period = 30
        self.action = ActionChains(self.driver)
        self.count = 0
        self.item_prices = []
        self.research_element = None
        self.cookie_upgrades = {}
        self.highest_price_affordable_building = 0
        self.user_input = ""

    def getDriver(self):
        return self.driver

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

    def startup(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID,"langSelect-EN")))
        # opening lang select screen
        self.lang = self.driver.find_element(by="id", value="langSelect-EN")
        self.proper_click(self.lang)


        # this is our cookie. It's gonna get clicked alot.
        self.cookie = self.driver.find_element(by="id", value="bigCookie")

        # finding file latest save from downloads and uses it
        self.startup = True
        self.path = r"C:\Users\Zlswo\Downloads"
        self.list_of_files = glob.glob(f"{self.path}\ScienceRobotBakery*")
        print(self.list_of_files)
        self.latest_file = max(self.list_of_files, key=os.path.getctime)
        print(f"lastest file is {self.latest_file}. LOADING THIS FILE.")

        #launching screen, often takes a refresh
        while self.startup == True:
            try:
                self.items = self.driver.find_elements(by="css selector", value="#store div")
                self.item_ids = [self.item.get_attribute("id") for self.item in self.items]
            except:
                print("trying refresh")
                time.sleep(7)
                self.driver.refresh()
            else:
                print("page loaded!")
                print("clicking options")
                WebDriverWait(self.driver, 20).until((EC.element_to_be_clickable((By.CSS_SELECTOR, "#prefsButton"))))
                self.options = self.driver.find_element(by="css selector", value="#prefsButton")
                self.proper_click(self.options)
                print("loading file...")
                # WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "FileLoadInput"))).send_keys(
                #     self.latest_file)
                self.driver.find_element(by="id", value="FileLoadInput").send_keys(self.latest_file)
                self.startup = False
                print("startup ending! Moving on")

    def main_click(self):
        try:
            self.cookie.click()
        except:
            time.sleep(3)
            self.cookie = self.driver.find_element(by="id", value="bigCookie")
            self.proper_click(self.cookie)

    def elder_pledge(self):
        print("Starting: elder_pledge")
        try:
            self.elder_element = self.driver.find_element(by="css selector",
                                                         value="#toggleUpgrades div[data-id='74']")
            print(f"Elder Pledge is: {self.elder_element}")
        except NoSuchElementException:
            print("No Elder Pledge found!")
            pass
        except:
            traceback.print_exc()
        else:
            print("clicking tech element")
            self.proper_click(self.elder_element)


    def find_tech(self):
        print("Starting: find_tech")
        try:
            self.tech_element = self.driver.find_element(by="css selector", value="#techUpgrades .crate.upgrade.enabled")
            print(f"Tech element is: {self.tech_element}")
        except NoSuchElementException:
            print("No Tech found!")
            pass
        except StaleElementReferenceException:
            self.tech_element = self.driver.find_element(by="css selector", value="#techUpgrades .crate.upgrade.enabled")
        except:
            traceback.print_exc()
        else:
            print("clicking tech element")
            self.proper_click(self.tech_element)
            time.sleep(.5)
            if EC.presence_of_element_located((By.CSS_SELECTOR,"#promptContentRequiresConfirmation")):
                print("Found a prompt!")
                string = "purchasing this will have unexpected"
                try:
                    ft_ele_text = self.driver.find_element(By.CSS_SELECTOR, "#promptContentRequiresConfirmation .block").text
                    ft_ele = self.driver.find_element(By.CSS_SELECTOR, "#promptOption0")
                    # self.action.move_to_element(self.ft_ele).click().perform()
                    if string in ft_ele_text:
                        self.action.move_to_element(ft_ele).click().perform()
                        print("Bring on the GMAMAMAMAMAS")
                except:
                    traceback.print_exc()

    def find_research(self):
        print("Starting: find_research")
        total_eles = self.driver.find_elements(by="css selector", value="#upgrades .crate.upgrade.enabled")
        research_len = len(total_eles)
        if research_len > 5:
            buy_all = self.driver.find_element(by="css selector", value="#storeBuyAll")
            try:
                self.action.move_to_element(buy_all).click(buy_all).perform()
            except:
                traceback.print_exc()
            else:
                research_len = 0
        print(f"Research len is {research_len}")
        for i in range(0, research_len):
            try:
                self.research_element = self.driver.find_element(by="css selector", value="#upgrades .crate.upgrade.enabled")
            except NoSuchElementException:
                pass
            except StaleElementReferenceException:
                traceback.print_exc()
                pass
            except:
                traceback.print_exc()
            else:
                self.proper_click(self.research_element)
                self.action.click().pause(.1).perform()

    # gets the prices of the store items
    def get_prices(self):
        print("Starting: Get Prices")
        self.item_prices.clear()
        self.all_prices = self.driver.find_elements(by="css selector", value=".product.unlocked .price")
        print(f"all prices is: {self.all_prices}")
        # Convert <b> text into an integer price.
        for price in self.all_prices:
            try:
                self.element_text = price.text
                if self.element_text != "":
                    self.temp = self.element_text.strip().replace(",", "")
                    self.cost = float(self.temp)
                    self.item_prices.append(self.cost)
            except StaleElementReferenceException:
                print("Stale element in get prices!")
            except:
                traceback.print_exc()
        print(f"ITem_prices is: {self.item_prices}")


    def find_items(self):
        print("Starting: find_items")
        # Create dictionary of store items and prices
        self.cookie_upgrades.clear()
        print(f"Item prices is: {self.item_prices}")
        for n in range(len(self.item_prices)):
            self.cookie_upgrades[self.item_prices[n]] = f"product{n}"
        print(f"cookie upgrades is: {self.cookie_upgrades}")

    # Find upgrades that we can currently afford
    def buildings_to_buy(self):
        print("Starting: upgrades_to_buy")
        self.get_cookie_count()
        self.building_upgrades_swapped = []
        for self.cost, id in self.cookie_upgrades.items():
            # if self.cookie_count > self.cost:  # removed and id not in self.ignore_list todo remove
            self.building_upgrades_swapped.append([id, self.cost])
        print(f"all upgrades is: {self.building_upgrades_swapped}")

    def purchase_buildings_swapped(self):
        self.buildings_purchased = 0
        self.btn_100 = self.driver.find_element(By.CSS_SELECTOR, "#storeBulk100")
        self.action.move_to_element(self.btn_100).pause(.5).click().perform()
        for building in reversed(self.building_upgrades_swapped):
            to_purchase_id = building[0]
            building_element = self.driver.find_element(by="id", value=to_purchase_id)
            self.action.move_to_element(building_element).click().perform()


    def timeout_sequence(self):
        print("Starting: timeout_sequence")
        self.close_notes()
        self.get_prices()
        self.find_tech()
        if self.count % 2 == 0:
            self.find_research()
        else:
            print("Skipping upgrade research")
        self.find_items()
        self.get_cookie_count()
        self.buildings_to_buy()
        self.purchase_buildings_swapped()
        if keyboard.is_pressed("~"):
            self.pause_func()
        self.find_tech()
        self.find_research()
        self.count += 1
        print(f"count is: {self.count}")
        self.close_notes()

    def get_cookie_count(self):
        print("Starting: get_cookie_count")
        # Get current cookie count
        self.element_check = self.driver.find_element(by="id", value="cookies").text
        # print(f"Ele check for current count is: {self.element_check}")
        self.money_element = self.driver.find_element(by="id", value="cookies").text.strip().split("\n")[0].split(" ")[0].replace(
            ",", "").replace(".", "")
        self.cookie_count = float(self.money_element)/100
        print(f"Cookie count is: {self.cookie_count}")

    def close_notes(self):
        # closes achievement notes
        while True:
            try:
                if EC.presence_of_element_located((By.CSS_SELECTOR, "#notes .close")):
                    print("found thing to close!")
                    self.close = self.driver.find_element(by="css selector", value="#notes .close")
                    self.proper_click(self.close)
                    print("closed it!")
            except StaleElementReferenceException:
                pass
            except NoSuchElementException:
                break
            except:
                traceback.print_exc()
                break

    def golden_cookie_check(self):
        self.gc = self.driver.find_elements(by="css selector", value=".shimmer")
        print(len(self.gc))

        if len(self.gc) != 0:
            print("I found gc")
            self.action.move_to_element(self.gc[0]).perform()
            self.action.click().perform()
            print("I found a golden cookie and clicked it!")

    def pause_func(self):  # todo fix
        print("Game Paused!")
        while True:
            time.sleep(.1)
            if keyboard.is_pressed("~"):
                print("Ending pause")
                break

    def stop_func(self):
        while True:
            self.user_input = input("What would you like to do? (pause, wait, timeout, elder, upgrade, exit)").lower()
            if self.user_input == "timeout":
                self.timeout_sequence()
                break
            elif self.user_input == "pause":
                print("Press ~ to unpause")
                self.pause_func()
                break
            elif self.user_input == "wait":
                self.wait_period = int(input("Enter a new wait period (int): "))
                if type(self.wait_period) == int:
                    break
                else:
                    self.wait_period = 30
            elif self.user_input == "elder":
                self.elder_pledge()
                break
            elif self.user_input == "upgrade":
                self.find_research()
                break
            elif self.user_input == "garden":
                break
            elif self.user_input == "exit":
                break
            else:
                pass

    def save_file(self):
        try:
            self.stats_menu = self.driver.find_element(by="css selector", value="#statsButton")
            self.options_menu = self.driver.find_element(by="css selector", value="#prefsButton")
            self.proper_click(self.stats_menu)
            self.proper_click(self.options_menu)
            save = self.driver.find_element(by="css selector",
                                                 value=r'''.subsection a.option.smallFancyButton[onclick="Game.FileSave();PlaySound('snd/tick.mp3');"''')
            self.proper_click(save)
            self.proper_click(self.stats_menu)
            print("file saved!")
        except NoSuchElementException:
            traceback.print_exc()
            print("was not able to save!")
            self.proper_click(self.stats_menu)
        except StaleElementReferenceException:
            print("Stale Element found, retrying")
            self.save_file()
        except:
            traceback.print_exc()
            self.proper_click(self.stats_menu)

    def close_menus(self):
        try:
            if EC.presence_of_element_located((By.CSS_SELECTOR,"#prefsButton.selected")):
                menu = self.driver.find_element(By.CSS_SELECTOR,"#prefsButton.selected")
                self.proper_click(menu)
        except NoSuchElementException:
            pass
        try:
            if EC.presence_of_element_located((By.CSS_SELECTOR,"#statsButton.selected")):
                menu = self.driver.find_element(By.CSS_SELECTOR,"#statsButton.selected")
                self.proper_click(menu)
        except NoSuchElementException:
            pass
        try:
            if EC.presence_of_element_located((By.CSS_SELECTOR,"#logButton.selected")):
                menu = self.driver.find_element(By.CSS_SELECTOR,"#logButton.selected")
                self.proper_click(menu)
        except NoSuchElementException:
            pass
        try:
            if EC.presence_of_element_located((By.CSS_SELECTOR,"#legacyButton.selected")):
                menu = self.driver.find_element(By.CSS_SELECTOR,"#legacyButton.selected")
                self.proper_click(menu)
        except NoSuchElementException:
            pass
        except:
            traceback.print_exc()
