from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from .constants import (
    BASE_URL,
    DEFAULT_TIMEOUT_SECONDS,
    IMPLICIT_WAIT_SECONDS,
    INACTIVE_DAYS_THRESHOLD,
    MIN_LEVEL_FOR_ACTIVITY,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from prettytable import PrettyTable


class LOL:
    def __init__(self, region, username, tag):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver_path = 'chromedriver.exe'
        self.driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=options)
        self.__summoner_name = f"{username}#{tag}"
        self.__region = region
        self.__active = "Active"
        self.__profile_summoner_url = f"{BASE_URL}/{region.lower()}/{username.lower()}-{tag.lower()}/overview"
        self.driver.get(self.__profile_summoner_url)
        self.driver.implicitly_wait(IMPLICIT_WAIT_SECONDS)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.driver.quit()

    def update_stat(self):
        try:
            WebDriverWait(self.driver, DEFAULT_TIMEOUT_SECONDS).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button[class='update-button']")
                )
            )
            update_btn = self.driver.find_element(by=By.CSS_SELECTOR, value="button[class='update-button']")
            update_btn.click()
            WebDriverWait(self.driver, DEFAULT_TIMEOUT_SECONDS).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button[class='update-button']")
                )
            )
        except TimeoutException:
            # Keep behavior resilient if the page cannot be updated.
            return

    def get_level_summoner(self):
        level_text = self.driver.find_element(
            by=By.CLASS_NAME, value="level-header"
        ).text
        return int(level_text)

    def last_match_played(self):
        matches = self.driver.find_elements(by=By.CLASS_NAME, value="content-container")
        if not matches:
            return None
        last_match = matches[0]
        status = last_match.find_element(by=By.CLASS_NAME, value="victory-status").get_attribute("innerHTML")
        match_type = last_match.find_element(by=By.CLASS_NAME, value="queue-type").get_attribute("innerHTML")
        from_when = last_match.find_element(by=By.CLASS_NAME, value="from-now").get_attribute("innerHTML")

        return match_type, status, from_when

    @staticmethod
    def _extract_days(from_when):
        if not from_when:
            return None
        parts = from_when.split()
        if not parts:
            return None
        if "day" not in from_when and "days" not in from_when:
            return None
        try:
            return int(parts[0])
        except (TypeError, ValueError):
            return None

    def is_active(self):
        last_match = self.last_match_played()
        if not last_match:
            return False

        from_when = last_match[-1]
        level = self.get_level_summoner()
        num_days = self._extract_days(from_when)
        if num_days is not None:
            if num_days >= INACTIVE_DAYS_THRESHOLD and level < MIN_LEVEL_FOR_ACTIVITY:
                return False
        return True

    def all_match_played(self):
        matches_result = []
        matches = self.driver.find_elements(by=By.CLASS_NAME, value="content-container")

        for i in range(0, len(matches), 2):
            try:
                status = matches[i].find_element(by=By.CLASS_NAME, value="victory-status").get_attribute("innerHTML")
                match_type = matches[i].find_element(by=By.CLASS_NAME, value="queue-type").get_attribute("innerHTML")
                from_when = matches[i].find_element(by=By.CLASS_NAME, value="from-now").get_attribute("innerHTML")
                matches_result.append(
                    [match_type, status, from_when]
                )
            except NoSuchElementException:
                continue
        return matches_result

    def decide_active(self):
        active = self.is_active()
        if not active:
            self.__active = "InActive"

    @property
    def summoner_name(self):
        return self.__summoner_name

    @property
    def active(self):
        return self.__active

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
            table.add_row(
                ["No Matches Found", "No Matches Found", "No Matches Found"]
            )
        else:
            table.add_rows(
                result_all_matches
            )
        return table
