from abc import abstractmethod


class HttpProxyBase:
    @abstractmethod
    def get_proxy(self):
        pass
