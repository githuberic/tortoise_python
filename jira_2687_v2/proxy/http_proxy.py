from jira_2687_v2.proxy.base.http_proxy_base import HttpProxyBase


class HttpProxy(HttpProxyBase):
    def __init__(self, server, port, user_name, password):
        self.server = server;
        self.port = port;
        self.user_name = user_name
        self.password = password

    def get_proxy(self):
        url_proxy = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": self.server,
            "port": self.port,
            "user": self.user_name,
            "pass": self.password,
        }

        proxy_handler = {'http': url_proxy, 'https': url_proxy}

        return proxy_handler
