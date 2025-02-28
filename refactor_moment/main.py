import typing
import requests
import time
from abc import ABC, abstractmethod
import undetected_chromedriver as uc
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


class SeleniumFetcher(WebFetcherInterface):
    def __init__(self, url_provider: UrlProvider, driver_manager: SeleniumWebDriverManager) -> None:
        self.url_provider = url_provider
        self.driver_manager = driver_manager

    def create_request(self):
        driver = self.driver_manager.get_driver()
        driver.get(self.url_provider.get_url())

    def get_request(self):
        time.sleep(8)
        return self.driver_manager.get_driver().page_source


class RequestFetcher(WebFetcherInterface):
    def __init__(self, url_provider: UrlProvider, connect_proxies: ConnectProxies,
                 create_headers: CreateHeaders) -> None:
        self.url_provider = url_provider
        self.proxies = connect_proxies.create_connection()
        self.headers = create_headers.get_headers()
        self.response = None

    def create_request(self):
        url = self.url_provider.get_url()
        self.response = requests.get(url, proxies=self.proxies, timeout=10, headers=self.headers)

    def get_request(self):
        if self.response:
            return self.response.text
        return None


url_provider = UrlProvider("http://httpbin.org/ip")

# Для работы с прокси и заголовками
request_fetcher = RequestFetcher(url_provider, ConnectProxies(False), CreateHeaders())
request_fetcher.create_request()
print(request_fetcher.get_request())

# Для работы с Selenium
selenium_fetcher = SeleniumFetcher(url_provider, SeleniumWebDriverManager())
selenium_fetcher.create_request()
print(selenium_fetcher.get_request())
