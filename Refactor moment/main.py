import typing
import requests
from proxies_settings import ConnectProxies


class CreateHeaders:
    def __init__(self) -> None:
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_headers(self):
        return self.headers


class WebPageFetcher:
    def __init__(self, url: str, connectProxies : ConnectProxies, createHeaders: CreateHeaders) -> None:
        self.url = url
        self.proxies = connectProxies.create_connection()
        self.headers = createHeaders.get_headers()
        self.response = None

    def create_request(self):
        self.response = requests.get(self.url, proxies=self.proxies, timeout=10,
                                     headers=self.headers)

    def get_request(self):
        return self.response.text


startParser = WebPageFetcher("http://httpbin.org/ip", ConnectProxies(False), CreateHeaders())
startParser.create_request()
print(startParser.get_request())
