import time

import pandas as pd
from driver_functions import get_articles, get_articles_basic, set_up_driver
from selenium.webdriver.common.by import By

driver = set_up_driver()
driver.get("https://trumpwhitehouse.archives.gov/briefings-statements/")
time.sleep(10)
df = pd.DataFrame(columns=["date", "brief_format", "header", "text", "url"])

number_of_pages = driver.find_element(
    By.XPATH, "/html/body/div[1]/main/div[2]/div/div/a[3]"
).text
# number_of_pages = number_of_pages.split('\n')[1]

for page_number in range(0, int(number_of_pages) - 2):
    df_new = get_articles(driver, df, page_number)
    driver.get(
        "https://trumpwhitehouse.archives.gov/briefings-statements/page/{}/".format(
            page_number + 2
        )
    )
    time.sleep(10)
    df.to_csv("wh_articles_trump_long.csv", index=False)

driver.quit()
