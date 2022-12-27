import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def set_up_driver() -> webdriver:
    driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    options = Options()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--start-maximized")
    # options.add_argument('--headless')

    driver = webdriver.Edge(options=options)

    return driver


def get_articles_basic(driver, df, page_number) -> pd.DataFrame:
    for article_number in range(0, 10):
        try:
            header = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/main/div[2]/div/article[{}]/div/h2/a".format(
                    article_number + 1
                ),
            ).text
            date = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/main/div[2]/div/article[{}]/div/div/p/time".format(
                    article_number + 1
                ),
            ).text
            brief_format = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/main/div[2]/div/article[{}]/div/p".format(
                    article_number + 1
                ),
            ).text
            url = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/main/div[2]/div/article[{}]/div/h2/a".format(
                    article_number + 1
                ),
            ).get_attribute("href")

            df.loc[len(df) + 1] = [date, brief_format, header, url]

        except Exception as e:
            if "NoSuchWindowException" in str(e.__class__):
                driver = set_up_driver()
                driver.get(
                    "https://www.whitehouse.gov/briefing-room/page/{}/".format(
                        page_number + 2
                    )
                )
                time.sleep(5)
            else:
                print(e)

    return df


def get_articles(driver, df, page_number) -> pd.DataFrame:
    for article_number in range(0, 10):
        try:
            driver.execute_script(
                "window.scrollTo(0, {});".format(article_number * 1000)
            )
            time.sleep(2)
            url = driver.find_element(
                By.XPATH,
                "/html/body/div[1]/main/div[2]/div/article[{}]/div/h2/a".format(
                    article_number + 1
                ),
            ).get_attribute("href")
            driver.get(url)
            time.sleep(5)

            brief_format = driver.find_element(
                By.XPATH, "/html/body/div[1]/main/div[1]/div/p"
            ).text
            date = driver.find_element(
                By.XPATH, "/html/body/div[1]/main/div[1]/div/div/p/time"
            ).text
            header = driver.find_element(
                By.XPATH, "/html/body/div[1]/main/div[1]/div/h1"
            ).text
            text = driver.find_element(
                By.XPATH, "/html/body/div[1]/main/div[2]/div/div"
            ).text
            text = text.replace('"', "'")

            df.loc[len(df) + 1] = [date, brief_format, header, text, url]

            driver.back()
            time.sleep(5)
        except Exception as e:
            if "NoSuchWindowException" in str(e.__class__):
                driver = set_up_driver()
                driver.get(
                    "https://trumpwhitehouse.archives.gov/briefings-statements/page/{}/".format(
                        page_number + 2
                    )
                )
                time.sleep(5)
            else:
                print(e)
    return df
