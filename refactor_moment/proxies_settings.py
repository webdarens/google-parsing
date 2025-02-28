import typing
import requests


class ConnectProxies:
    def __init__(self, do_connect) -> None:
        self.do_connect = do_connect
        self.proxy_url = 'socks5h://127.0.0.1:9150'
        self.proxies_settings = {}

    def create_connection(self):
        self.proxies_settings = {'http': self.proxy_url,
                                 'https': self.proxy_url, }
        return self.proxies_settings if self.do_connect else False
