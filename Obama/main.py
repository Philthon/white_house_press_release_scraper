import time

import pandas as pd
from driver_functions import get_articles, get_articles_basic, set_up_driver
from selenium.webdriver.common.by import By

driver = set_up_driver()
driver.get(
    "https://obamawhitehouse.archives.gov/briefing-room/statements-and-releases?term_node_tid_depth=41&page=0"
)
time.sleep(10)
df = pd.DataFrame(columns=["date", "brief_format", "header", "text", "url"])

number_of_pages = driver.find_element(
    By.XPATH, "/html/body/section/div[2]/div/div/div[2]/div[2]/div/div[2]/ul/li[2]"
).text
number_of_pages = number_of_pages.split("of ")[1]

for page_number in range(0, int(number_of_pages)):
    df_new = get_articles(driver, df, page_number)
    driver.get(
        "https://obamawhitehouse.archives.gov/briefing-room/statements-and-releases?term_node_tid_depth=41&page={}".format(
            page_number
        )
    )
    time.sleep(10)
    df.to_csv("wh_articles_obama_statement_and_releases_long.csv", index=False)

driver.quit()
