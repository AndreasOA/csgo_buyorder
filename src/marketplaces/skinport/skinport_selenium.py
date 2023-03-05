from selenium import webdriver
from selenium import *
import requests
import json
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from time import sleep
from src.utils.constants import Constans
import re


ai_f = open('misc/accepted_items.txt', 'r')
accepted_items = ai_f.read().replace("'", "").split("\n")
ai_f.close()

class Skinport:
    def __init__(self, username, password, language, ccs, telegram_api,
                 telegram_chat, phone, acceptable_discount, good_discount, 
                 debug = True, buy_item = False, notify_user = False) -> None:
        options = webdriver.ChromeOptions() 
        options.add_argument("user-data-dir=/Users/ao/Library/Application Support/Google/Chrome") #Path to your chrome profile
        options.add_argument("--no-proxy-server")
        options.add_argument("--disable-extensions")
        options.add_argument("disable-infobars")
        options.add_argument("--no-sandbox")
        #options.add_argument("--headless")
        self.driver = webdriver.Chrome(r'chromedriver', chrome_options=options)
        self.username = username
        self.password = password
        self.ccs = ccs
        self.language = language
        self.checked_items = []
        self.debug = debug
        self.buy_item = buy_item
        self.notify_user = notify_user
        self.isCartOpen = False
        ########################
        # Get Constants
        self.c = Constans(telegram_api, telegram_chat, phone, acceptable_discount, good_discount)
        ########################
        # Start
        self.driver.get('https://skinport.com')
        #self.driver.maximize_window()
        sleep(5)


    def login(self) -> None:
        try:
            self.driver.find_element_by_class_name('HeaderContainer-link--login').click()
            sleep(5)
            email_input = self.driver.find_element_by_id('email')
            email_input.send_keys(self.username)
            pw_input = self.driver.find_element_by_id('password')
            pw_input.send_keys(self.password)
            self.driver.find_element_by_class_name('SubmitButton').click()
            t = False
            while not t:
                try:
                    self.driver.find_element_by_class_name('Footer-lang')
                    t = True
                except:
                    sleep(5)
        except NoSuchElementException:
            print('already logged in')

    
    def changeLanguage(self) -> None:
        lan = self.driver.find_element_by_class_name('Footer-lang')
        lan_btn = lan.find_element_by_class_name('Dropdown-button')
        lan_btn.click()
        sleep(2)
        lan_dd = self.driver.find_element_by_class_name('Dropdown-dropDown-enter-done')
        try:
            lan_dd.find_element_by_class_name(self.language).click()
        except (NoSuchElementException, ElementClickInterceptedException):
            pass

        sleep(5)


    def setup(self):
        self.login()
        self.changeLanguage()


    def runMarketTracker(self):
        self.setup()
        self._activateLiveMarket()
        self._trackMarket()


    def _activateLiveMarket(self) -> None:
        self.driver.find_element_by_class_name('HeaderContainer-link--market').click()
        sleep(40)
        catalog_div = self.driver.find_element_by_class_name('CatalogPage-header')
        catalog_div.find_element_by_class_name('Dropdown-button').click()
        sleep(1)
        market_sort = self.driver.find_element_by_class_name('Dropdown-dropDown-enter-done')
        market_sort_children = market_sort.find_elements_by_class_name('Dropdown-itemText')
        market_sort_children[-1].click()
        sleep(2)
        self.driver.find_element_by_class_name('LiveBtn').click()
        sleep(1)


    def _openCart(self):
        self.driver.execute_script("window.open('https://skinport.com/cart')")
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[0])
        if self.debug:
            print('[status] - Cart Tab is open')
        self.isCartOpen = True


    def _trackMarket(self, runs = True) -> None:
        sleep(20)
        while runs:
            items = self.driver.find_elements_by_class_name('CatalogPage-item')
            for item in items:
                if item not in self.checked_items:
                    self.checked_items.append(item)
                    try:
                        label = item.find_element_by_class_name('ItemPreview-href')
                    except:
                        self.driver.switch_to.window(self.driver.window_handles[0])
                        sleep(1)
                        label = item.find_element_by_class_name('ItemPreview-href')
                    item_name = label.get_attribute("aria-label")
                    try:
                        item_name, item_cond = item_name.split(' (')
                    except ValueError:
                        item_cond = ' '
                    item_cond = item_cond[:-1]
                    try:
                        discount = item.find_element_by_class_name('ItemPreview-discount')
                        discount_value = discount.find_element_by_tag_name('span').text
                        discount_value = int(re.sub('[^0-9]','', discount_value))
                    except NoSuchElementException:
                       discount_value = 0

                    sugg_price = item.find_element_by_class_name('ItemPreview-oldPrice').text
                    sugg_price = float(sugg_price.replace('Suggested price ', '').replace('.', '').replace(' €', '').replace(',', '.'))
                    real_price = item.find_element_by_class_name('ItemPreview-priceValue').find_element_by_class_name('Tooltip-link').text
                    real_price = float(real_price.replace('.', '').replace(' €', '').replace(',', '.'))
                    if self.debug:
                        print('=====================================')
                        print(f"ITEM: {item_name}\nPRICE: {real_price}€\nOLD PRICE: {sugg_price}€\nDISCOUNT: {discount_value}%")
                        print('=====================================')

                    if sugg_price >= 3:
                        if discount_value >= 30 or (item_name in accepted_items and ((item_name.find('★ ') != -1 and discount_value >= 25 and 'Doppler' not in item_name) or discount_value >= 29)):
                            try:
                                if self.buy_item:
                                    self._addItemToCart(item)
                                if self.notify_user:
                                    self._notifyUser(item_name, discount_value, real_price, sugg_price)
                            except NoSuchElementException:
                                self.driver.switch_to.window(self.driver.window_handles[0])
    

    def _addItemToCart(self, item):
        shop_item = ActionChains(self.driver).move_to_element(item)
        shop_item.perform()
        item.find_element_by_class_name('ItemPreview-mainAction').click()
        sleep(0.2)


    def _checkout(self):
        if self.isCartOpen:
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.refresh()
            checkboxes = self.driver.find_elements_by_class_name("Checkbox-input")
            for checkbox in checkboxes:
                checkbox.click()
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "SubmitButton"))).click()
            checkout =   WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME,"CommonLayout-checkout-enter-done")))
            cvc_parent = checkout.find_element_by_class_name("adyen-checkout__card__cvc__input")
            i_frame = cvc_parent.find_element_by_class_name('js-iframe')
            self.driver.switch_to.frame(i_frame)
            sleep(1)
            self.driver.find_element_by_class_name('gsf-holder').find_element_by_tag_name('input').send_keys(self.ccs)
            self.driver.switch_to.default_content()
            sleep(1)
            self.driver.find_element_by_class_name('adyen-checkout__button--pay').click()

    
    def _notifyUser(self, item_name, discount_value, curr_price, sugg_price):
        requests.get(self.c.getTelegramURL()+f'{item_name} - {discount_value}% /// {curr_price}/{sugg_price}').json()


if __name__ == "__main__":
    f = open("misc/credentials_adv.json")
    data = json.load(f)
    f.close()

    t_api = data['telegram']['api_token']
    t_id = data['telegram']['chat_id']
    phone = ''

    skinportMarketTracker = Skinport(data['skinport_api_credentials']['username'], 
                                        data['skinport_api_credentials']['password'],
                                        'GB',
                                        data['cc']['secret'], 
                                        t_api,
                                        t_id,
                                        phone,
                                        0.25,
                                        0.3,
                                        True, 
                                        True,
                                        True
                                        )
    skinportMarketTracker.runMarketTracker()
