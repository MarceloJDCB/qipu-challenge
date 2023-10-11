import logging
import os
import time
import urllib
from datetime import date, datetime

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class AisWebDriverManager:
    def __init__(
            self,
            profile_path: str = os.getcwd(),
            ais_url: str = "https://aisweb.decea.mil.br/",
            webdriver_timeout_seconds: int = 100,
            options_argument: list = [
                '--no-sandbox',
                '--headless',
                '--disable-gpu',
                '--disable-extensions',
                '--disable-infobars',
                '--start-maximized',
                '--disable-notifications',
                '--disable-dev-shm-usage',
            ]
    ) -> webdriver.Chrome:
        logging.basicConfig(
            filename=f"{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.log",
            encoding='utf-8',
            level=logging.INFO
        )
        self.ais_url = ais_url
        self.profile_path = profile_path
        options = webdriver.ChromeOptions()
        for argument in options_argument:
            options.add_argument(argument)
        self.webdriver_timeout_seconds = webdriver_timeout_seconds
        self.driver = webdriver.Remote(
            command_executor="http://chrome:4444/wd/hub",
            options=options
        )

    def sync_webpage(self, endpoint: str, tries: int = 0, max_tries: int = 3):
        self.driver.get(f"{self.ais_url}{endpoint}")
        try:
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.ID, "header"))
            )
        except Exception as er:
            if tries == max_tries:
                print(f"Max tries reached: {er}")
                self.quit_driver()
            self.sync_webpage(tries+1)

    def quit_driver(self) -> bool:
        self.driver.quit()
        return True


class AisElementGetter:
    def __init__(
        self,
        driver: webdriver.Chrome,
        action_delay_seconds: int = 0
    ):
        self.action_delay_seconds = action_delay_seconds
        self.driver = driver

    def _ais_pattern(fn):
        def wrapper(self, *args, **kwargs):
            try:
                result = fn(self, *args, **kwargs)
                time.sleep(self.action_delay_seconds)
                return result
            except Exception as er:
                print(f"Error: {er}")
                self.driver.quit()
        return wrapper

    @_ais_pattern
    def find_element(self, by, value) -> WebElement:
        return WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(
                    (by, value)
                )
            )

    @_ais_pattern
    def get_table_df(self, by, value) -> pd.DataFrame:
        table = self.find_element(by, value)
        soup = BeautifulSoup(table.get_attribute('outerHTML'), "html.parser")
        table_headers = []
        for th in soup.find_all('th'):
            th_text = th.text
            if th_text:
                table_headers.append(th_text)

        table_data = []
        for row in soup.find_all('tr'):
            columns = row.find_all('td')
            output_row = []
            for column in columns:
                text = column.text
                if text:
                    output_row.append(text.replace("\n", " "))
            if output_row:
                table_data.append(output_row)
        
        try:
            return pd.DataFrame(table_data, columns=table_headers)
        except ValueError:
            return pd.DataFrame()


class AisScraping:
    def __init__(self, icao: str):
        self.check_site_connection()
        self.ais_manager = AisWebDriverManager()
        self.icao = icao
        self.element_getter = AisElementGetter(self.ais_manager.driver)

    def get_cards(self):
        self.ais_manager.sync_webpage("?i=cartas")
        icao_code_input = self.element_getter.find_element(
            By.XPATH, "//input[contains(@name, 'icaocode')]"
        )
        get_table_btn = self.element_getter.find_element(
            By.XPATH, "//input[contains(@value, 'Filtrar')]"
        )
        icao_code_input.send_keys(self.icao)
        get_table_btn.click()
        df_table = self.element_getter.get_table_df(
            By.XPATH, "//table[contains(@id, 'datatable')]"
        )
        return df_table.Carta.to_list() if not df_table.empty else []

    def get_aerodrome_info(self) -> dict:
        self.ais_manager.sync_webpage(f"?i=aerodromos&codigo={self.icao}")
        metar = self.element_getter.find_element(
            By.XPATH, "//h5[text()='METAR']/following-sibling::p[1]"
        )
        taf = self.element_getter.find_element(
            By.XPATH, "//h5[text()='TAF']/following-sibling::p[1]"
        )
        sunset = self.element_getter.find_element(
            By.XPATH, "//sunset"
        )
        sunrise = self.element_getter.find_element(
            By.XPATH, "//sunrise"
        )
        return {
            "metar": metar.text,
            "taf": taf.text,
            "sunset": sunset.text,
            "sunrise": sunrise.text,
        }

    def check_site_connection(self):
        try:
            urllib.request.urlopen('https://aisweb.decea.mil.br/')
        except Exception:
            raise Exception("Sem conexão com a internet / Site indisponível")

    def end_operation(self):
        self.ais_manager.quit_driver()


if __name__ == "__main__":
    print("""
      ,---.  ,--. ,---.  ,--.   ,--.,------.,-----.                                                ,--.
     /  O  \ |  |'   .-' |  |   |  ||  .---'|  |) /_      ,---.  ,---.,--.--. ,--,--. ,---.  ,---. `--',--,--,  ,---.
    |  .-.  ||  |`.  `-. |  |.'.|  ||  `--, |  .-.  \    (  .-' | .--'|  .--'' ,-.  || .-. || .-. |,--.|      \| .-. |
    |  | |  ||  |.-'    ||   ,'.   ||  `---.|  '--' /    .-'  `)\ `--.|  |   \ '-'  || '-' '| '-' '|  ||  ||  |' '-' '
    `--' `--'`--'`-----' '--'   '--'`------'`------'     `----'  `---'`--'    `--`--'|  |-' |  |-' `--'`--''--'.`-  /
                                                                                     `--'   `--'               `---'
    """)
    print('         _          ')
    print('         -=\`\      ')
    print('     |\ ____\_\__   ')
    print('   -=\c`""""""" "`) ')
    print('      `~~~~~/ /~~`  ')
    print('        -==/ /      ')
    print('          "-"       ')
    print(f"Data: {date.today().strftime('%d/%m/%Y')} / Hora: {datetime.now().strftime('%H:%M:%S')}")
    print("")
    icao = input("Insira o ICAO: ")
    ais = AisScraping(icao=icao)
    aerodrome_info = ais.get_aerodrome_info()
    if aerodrome_info:
        print("")
        print(f"Nascer do Sol: {aerodrome_info.get('sunrise')}")
        print(f"Pôr do Sol: {aerodrome_info.get('sunset')}")
        print(f"METAR: {aerodrome_info.get('metar')}")
        print(f"TAF: {aerodrome_info.get('taf')} \n")
        cards = ais.get_cards()
        print("Cartas disponiveis:")
        for i, card in enumerate(cards):
            print(f"{i+1} - {card}")
    else:
        print("Aerodromo não encontrado")
    ais.end_operation()
