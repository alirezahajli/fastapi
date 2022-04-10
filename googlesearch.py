import logging
from typing import Dict

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager import driver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


logging.basicConfig(level=logging.WARNING)


class FetchGoogleSearchResult(dict):
    def __init__(self, query: str, number_of_page: int) -> None:
        super().__init__()
        self.query = query
        self.number_of_page = number_of_page

    def set_up_driver(self):
        # service = Service(ChromeDriverManager().install())  # local
        # driver = webdriver.Chrome(service=service)  # local
        # driver.maximize_window()  # local
        chrome_opt = webdriver.ChromeOptions()
        chrome_opt.add_argument("--headless")
        chrome_opt.add_argument("--no-sandbox")

        driver = webdriver.Chrome("./chromedriver", options=chrome_opt)

        return driver

    @property
    def fetch(self) -> Dict:

        driver = self.set_up_driver()
        for page in range(1, self.number_of_page + 1):
            url = (
                "http://www.google.com/search?q="
                + self.query
                + "&start="
                + str((page - 1) * 5)
            )
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            result_sites = soup.find_all("div", class_="g")
            for result_site in result_sites:

                self[self.get_link(result_site.find("div", class_="TbwUpd NJjxre"))] = {
                    "title": self.get_title(
                        result_site.find("h3", class_="LC20lb MBeuO DKV0Md")
                    ),
                    "description": self.get_description(
                        result_site.find(
                            "div", class_="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf"
                        )
                    ),
                    "link": self.get_link(
                        result_site.find("div", class_="TbwUpd NJjxre")
                    ),
                }

        driver.close()
        return self

    def get_link(self, messy_link) -> str:
        if str(messy_link) != "None":
            messy_link = str(messy_link).split("<")[2]
            regular_link = messy_link.split(">")[1]
            return regular_link

    def get_description(self, messy_description) -> str:
        try:
            if len(messy_description.find_all("span")) > 1:
                return messy_description.find_all("span")[-1].get_text()
            return messy_description.find_all("span")[0].get_text()
        except Exception as e:
            logging.warning(e)
            return " "

    def get_title(self, messy_title) -> str:
        if str(messy_title) != "None":
            regular_title = str(messy_title).split(">")[1][:-4]
            return regular_title
        return self.query
