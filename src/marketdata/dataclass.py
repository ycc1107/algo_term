import attr
import time
import hashlib
import hmac
import datetime
import base64
import urllib
from abc import ABCMeta, abstractmethod

class ExchangeBase(metaclass=ABCMeta):
    def __init__(self, **kwargs):
        self.date            = datetime.date.today()
        self.base_url        = kwargs.pop("base_url", "")
        self.endpoint        = kwargs.pop("endpoint", "")
        self.api_key         = kwargs.pop("api_key", "")
        self.secret_key      = kwargs.pop("secret_key", "")
        self.passphrase      = kwargs.pop("passphrase", "")
        self.endpoint_name   = kwargs.pop("endpoint_name", "")
        self.symbols         = ["BTC-USDT", "ETH-USDT"]
        self.sleep_time      = 0.1

    @abstractmethod
    def creatRequet(self):
        pass
    
    @abstractmethod
    def getPath(self):
        pass

    def process(self, data):
        return data

class OKExOrder(ExchangeBase):
    def creatRequet(self):
        message = F"{str(time.time()[:13])}GET{self.endpoint}"
        mac = hmac.new(bytes(self.secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        sign = base64.b64encode(mac.digest())
        header = {
            "Content-Type":         "application/json",
            "OK-ACCESS-KEY":        self.api_key,
            "OK_ACCESS_SIGN":       sign,
            "OK-ACCESS-PASSPHRASE": self.passphrase,
        }
        while True:
            header["OK-ACCESS-TIMESTAMP"] = str(time.time()[:13])
            for url in self.getPath():
                yield url, header

class OKExSpotMarketData(ExchangeBase):
    def getPath(self):
        for sym in self.symbols:
            yield self.base_url + F"{self.endpoint}/{sym}/{self.endpoint_name}"
    
    def creatRequet(self):
        while True:
            for url in self.getPath():
                yield url, {}