from selenium import webdriver
from selenium.webdriver.common.by import By
import time

timeout = time.time() + 5                # every 5 seconds
stop_time = time.time() + 60 * 5        # 5 minutes

# keeping chrome open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

# find the cookie in webpage
find_cookie = driver.find_element(By.ID, value="cookie")

# finds the store & item ids
items = driver.find_elements(by=By.CSS_SELECTOR, value="#store div")
item_ids = [item.get_attribute("id") for item in items]
# print(item_ids)

game_is_on = True

while game_is_on:
    find_cookie.click()             # clicks on the cookie

    if time.time() > timeout:

        # gets prices as an int, stores in list
        all_prices = driver.find_elements(by=By.CSS_SELECTOR, value="#store b")
        item_prices = []
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)
        # print(item_prices)

        # combines item_prices & item_ids into one dictionary
        store_upgrades = {}
        for n in range(len(item_prices)):
            store_upgrades[item_prices[n]] = item_ids[n]


        # current cookie(money) count
        current_money = driver.find_element(By.ID, value="money").text
        current_money = int(current_money)

        # buys highest priced item we can afford
        affordable_upgrades = {}
        for cost, id in store_upgrades.items():
            if current_money > cost:
                affordable_upgrades[cost] = id
        # print(affordable_upgrades)


        highest_price_affordable_upgrade = max(affordable_upgrades, default=0)
        try:
            # print(highest_price_affordable_upgrade)
            item_to_buy = affordable_upgrades[highest_price_affordable_upgrade]
            driver.find_element(By.ID, value=item_to_buy).click()
        except KeyError:
            pass


        # adds another 5 seconds until next timeout
        timeout = time.time() + 5

    if time.time() > stop_time:
        cookies_per_second = driver.find_element(By.ID, value="cps").text
        print(cookies_per_second)
        break

















