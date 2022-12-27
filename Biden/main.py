import time
from datetime import datetime

import pandas as pd
from driver_functions import get_articles, get_articles_basic, set_up_driver
from selenium.webdriver.common.by import By

driver = set_up_driver()
driver.get("https://www.whitehouse.gov/briefing-room/")
time.sleep(10)
df = pd.DataFrame(columns=["date", "brief_format", "header", "text", "url"])

number_of_pages = driver.find_element(
    By.XPATH, "/html/body/div[3]/main/section[1]/div/div/div[2]/ul/li[5]/a"
).text
number_of_pages = number_of_pages.split("\n")[1]

for page_number in range(0, int(number_of_pages)):
    df = get_articles(driver, df, page_number)
    driver.get(
        "https://www.whitehouse.gov/briefing-room/page/{}/".format(page_number + 2)
    )
    time.sleep(10)
    current_dateTime = datetime.now()
    df.to_csv("wh_articles_biden_long.csv", index=False)

driver.quit()
