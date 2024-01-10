import warnings
from time import sleep

import chromedriver_autoinstaller
from decouple import config
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

warnings.filterwarnings("ignore",
                        category=UserWarning,
                        module="chromedriver_autoinstaller")


class DataScraper:

    def __init__(self, start_date, end_date):
        """
        Initialize the DataScraper with the start and end dates.

        Args:
            start_date (str): The start date for data retrieval.
            end_date (str): The end date for data retrieval.
        """
        self.driver = self._initialize_driver()
        self.start_date = start_date
        self.end_date = end_date
        self.LOGINEMPRESA = config('loginEmpresa')
        self.LOGINUSUARIO = config('loginUsuario')
        self.LOGINSENHA = config('loginSenha')

    def _initialize_driver(self) -> WebDriver:
        """
        Initialize and configure the Selenium WebDriver for web scraping.

        Returns:
            WebDriver: The configured WebDriver instance.
        """
        chromedriver_autoinstaller.install()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": "/home/artbdr/Documents/tmk-data/",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")

        service = Service()
        driver = webdriver.Chrome(options=chrome_options, service=service)
        driver.maximize_window()

        return driver

    def login(self):
        """
        Perform login to a website and navigate to the desired page.
        """
        url = 'https://ezpoint.com.br'
        self.driver.get(url)

        self._fill_input('//*[@id="loginEmpresa"]', self.LOGINEMPRESA)
        self._fill_input('//*[@id="loginUsuario"]', self.LOGINUSUARIO)
        self._fill_input('//*[@id="loginSenha"]', self.LOGINSENHA)

        self.driver.find_element('xpath', '//*[@id="btnSubmit"]').click()

        self.driver.find_element(
            'xpath', '//*[@id="mudarLogo"]/div[2]/ul/li[3]/a/p/b').click()

        sleep(4)
        self.driver.find_element(
            'xpath', '//*[@id="formsExamples"]/ul/li[4]/a').click()

    def download_report(self):
        """
        Download a report from the website.
        """
        self.driver.find_element('xpath', '//*[@id="inicio"]').clear()
        self.driver.find_element('xpath', '//*[@id="fim"]').clear()

        self._fill_input('//*[@id="inicio"]', self.start_date)
        self._fill_input('//*[@id="fim"]', self.end_date)

        self.driver.find_element('xpath', '//*[@id="navegabilidade"]').click()

        self.driver.find_element(
            'xpath',
            '//*[@id="pagTable"]/tbody/tr/td/div/div[1]/div/a').click()

        self.driver.find_element(
            'xpath', '//*[@id="ui-accordion-accordion-header-0"]/a').click()

        sleep(2)

        dropdown = self.driver.find_element('xpath', '//*[@id="extensao"]')

        select = Select(dropdown)
        select.select_by_visible_text('XLSX')

        self.driver.find_element(
            'xpath', '//*[@id="btnBaixarRelatorio"]').click()
        sleep(2)

        element_xpath = '//*[@id="ajaxLoad3"]'

        wait = WebDriverWait(self.driver, 10000000)
        wait.until(
            EC.invisibility_of_element_located((By.XPATH, element_xpath)))

        sleep(5)

        while True:
            try:
                modal_download_input = self.driver.find_element(
                    'xpath', '//*[@id="modalDownload"]/div/div/div[3]/input')
                modal_download_input.click()
                modal_download_input.click()
                break
            except ElementNotInteractableException:
                continue

        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="modalDownload"]/div/div/div[3]/input')
            )
        )
        sleep(10)

    def _fill_input(self, xpath, value):
        """
        Fill an input field with the specified value.

        Args:
            xpath (str): The XPath of the input field.
            value (str): The value to be entered into the input field.
        """
        element = self.driver.find_element('xpath', xpath)
        element.clear()
        element.send_keys(value)

    def close(self):
        """
        Close the WebDriver and release resources.
        """
        self.driver.quit()


if __name__ == "__main__":
    pass
