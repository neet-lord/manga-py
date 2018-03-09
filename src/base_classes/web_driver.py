from selenium import webdriver  # need, if captcha detected
from src.fs import get_current_path, get_temp_path, is_file, dirname
from sys import platform
from zipfile import ZipFile
from requests import get
from os import chmod


class WebDriver:
    driver_version = '2.36'

    @staticmethod
    def is_win():
        return ~platform.find('win32')

    def download_drivder(self):
        url_prefix = 'https://chromedriver.storage.googleapis.com/'
        url = 'chromedriver_linux64.zip'
        if ~platform.find('darwin'):
            url = 'chromedriver_mac64.zip'
        if ~platform.find('win32'):
            url = 'chromedriver_win32.zip'

        path = get_temp_path('driver.zip')

        with open(path, 'wb') as driver:
            driver.write(get(url_prefix + self.driver_version + url).content)
            driver.close()
        with ZipFile(path) as file:
            file.extractall(dirname(self._driver_path()))

    def _driver_path(self):
        driver = get_current_path() + '/storage/'
        if self.is_win():
            driver += 'chromedriver.exe'
        else:
            driver += 'chromedriver'
        return driver

    def get_driver(self):
        driver_path = self._driver_path()
        if not is_file(driver_path):
            self.download_drivder()
        self.is_win() and chmod(driver_path, 0o755)
        driver = webdriver.Chrome(executable_path=driver_path)
        driver.set_window_size(500, 600)
        return driver
