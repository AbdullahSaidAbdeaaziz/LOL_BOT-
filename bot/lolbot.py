from selenium import webdriver
from .constants import BASE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from prettytable import PrettyTable
import os


class LOL(webdriver.Chrome):
    def __init__(self, region, username, tag):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver_path = 'chromedriver.exe'
        super().__init__(service=Service(executable_path=driver_path), options=options)
        self.__summoner_name = f"{username}#{tag}"
        self.__region = region[:-1]
        self.__active = "Active"
        self.__profile_summoner_url = f"{BASE_URL}/{region.lower()}/{username.lower()}-{tag.lower()}/overview"
        self.get(self.__profile_summoner_url)
        self.implicitly_wait(0.5)
        self.minimize_window()

    def update_stat(self):
        WebDriverWait(self, 30).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[class='update-button']")
            )
        )
        update_btn = self.find_element(by=By.CSS_SELECTOR, value="button[class='update-button']")
        update_btn.click()
        WebDriverWait(self, 30).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[class='update-button']")
            )
        )

    def get_level_summoner(self):
        return self.find_element(
            by=By.CLASS_NAME, value="level-header"
        ).text

    def last_match_played(self):
        matches = self.find_elements(by=By.CLASS_NAME, value="content-container")
        last_match = matches[0]
        status = last_match.find_element(by=By.CLASS_NAME, value="victory-status").get_attribute("innerHTML")
        match_type = last_match.find_element(by=By.CLASS_NAME, value="queue-type").get_attribute("innerHTML")
        from_when = last_match.find_element(by=By.CLASS_NAME, value="from-now").get_attribute("innerHTML")

        return match_type, status, from_when

    def is_active(self):
        last_match = self.last_match_played()
        time = last_match[-1]
        Level = int(self.get_level_summoner())
        NUMBER_OF_INACTIVE = 2
        if "days" in time:
            num_days = int(time.split()[0])
            if num_days >= NUMBER_OF_INACTIVE and Level < 30:
                return False
        return True

    def all_match_played(self):
        matches_result = []
        matches = self.find_elements(by=By.CLASS_NAME, value="content-container")

        for i in range(0, len(matches), 2):
            status = matches[i].find_element(by=By.CLASS_NAME, value="victory-status").get_attribute("innerHTML")
            match_type = matches[i].find_element(by=By.CLASS_NAME, value="queue-type").get_attribute("innerHTML")
            from_when = matches[i].find_element(by=By.CLASS_NAME, value="from-now").get_attribute("innerHTML")
            matches_result.append(
                [match_type, status, from_when]
            )
        return matches_result

    def decide_active(self):
        active = self.is_active()
        if not active:
            self.__active = "InActive"

    def output_summoner_info(self):
        result_all_matches = self.all_match_played()
        level = self.get_level_summoner()
        self.decide_active()

        table = PrettyTable(field_names=[
            "Match Type", "Match Status", "Play From"
        ],
            title=f"{self.__summoner_name} {self.__region} {self.__active} Level: {level}"
        )
        if not result_all_matches:
            table.add_rows(
                ["No Matches Found", "No Matches Found", "No Matches Found"]
            )
        else:
            table.add_rows(
                result_all_matches
            )
        self.display_in_file(table)

    def display_in_file(self, table):
        path_folder = r"./Summoners"
        if not self.is_active():
            self.__active = "InActive"

        if not os.path.exists(path_folder):
            os.makedirs(path_folder)

        path_folder_in_nor_active = fr"{path_folder}/{self.__active}s"
        if not os.path.exists(path_folder_in_nor_active):
            os.makedirs(path_folder_in_nor_active)

        with open(fr"{path_folder_in_nor_active}/{self.__summoner_name}.txt", "w") as file:
            file.write(table.get_string())
