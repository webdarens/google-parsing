import typing
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import requests
import time
from abc import ABC, abstractmethod
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait

from proxies_settings import ConnectProxies


class CreateHeaders:
    def __init__(self) -> None:
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_headers(self):
        return self.headers


class UrlProvider:
    def __init__(self, url: str) -> None:
        self.url = url

    def url_modifier(self):
        if not self.url.startswith("http://") and not self.url.startswith("https://"):
            self.url = "http://" + self.url

    def get_url(self) -> str:
        return self.url


class WebFetcherInterface(ABC):
    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def create_request(self):
        pass


class SeleniumWebDriverManager:
    def __init__(self):
        self.driver = uc.Chrome()

    def get_driver(self):
        return self.driver

    def quit_driver(self):
        return self.driver.quit()


class SeleniumFetcher(WebFetcherInterface):
    def __init__(self, url_provider: UrlProvider, driver_manager: SeleniumWebDriverManager) -> None:
        self.url_provider = url_provider
        self.driver_manager = driver_manager

    def create_request(self):
        driver = self.driver_manager.get_driver()
        driver.get(self.url_provider.get_url())
        # замена фиксированного ожидания на динамическое ожидание загрузки страницы
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except Exception as e:
            print(f"Ошибка ожидания загрузки страницы: {e}")

    def get_request(self):
        try:
            return self.driver_manager.get_driver().page_source
        except Exception as e:
            return f"An error occurred:\n{e}"


class RequestWebManager:
    def __init__(self, url_provider: UrlProvider, connect_proxies: ConnectProxies,
                 create_headers: CreateHeaders) -> None:
        self.url = url_provider.get_url()
        self.proxies = connect_proxies.create_connection()
        self.headers = create_headers.get_headers()

    def create_request(self):
        response = requests.get(self.url, proxies=self.proxies, timeout=10, headers=self.headers)
        return response


class RequestFetcher(WebFetcherInterface):
    def __init__(self, requestWebManager: RequestWebManager) -> None:
        self.request_web_manager = requestWebManager
        self.response = None

    def create_request(self):
        self.response = self.request_web_manager.create_request()

    def get_request(self):
        if self.response is None:
            return None
        return self.response.text


class UserInteract:
    def __init__(self, url, boolConnectProxy):
        self.url = url
        self.boolConnectProxy = boolConnectProxy

    def calls_func(self):
        # обработка Url
        url_provider = UrlProvider(self.url)
        url_provider.url_modifier()

        # Для работы с Request
        request_web_manager = RequestWebManager(url_provider, ConnectProxies(self.boolConnectProxy), CreateHeaders())
        request_fetcher = RequestFetcher(request_web_manager)
        request_fetcher.create_request()
        print(request_fetcher.get_request())

        # Для работы с Selenium
        selenium_fetcher = SeleniumFetcher(url_provider, SeleniumWebDriverManager())
        selenium_fetcher.create_request()
        print(selenium_fetcher.get_request())


if __name__ == '__main__':
    # url = input()
    # boolConnectProxy = bool(int(input()))
    # userInteract = UserInteract(url, boolConnectProxy)
    # print(userInteract.calls_func())

    url = "http://httpbin.org/ip"
    boolConnectProxy = False
    userInteract = UserInteract(url, boolConnectProxy)
    print(userInteract.calls_func())
