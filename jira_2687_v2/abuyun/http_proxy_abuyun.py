from jira_2687_v2.proxy.http_proxy import HttpProxy


class HttpProxyAbuyun(HttpProxy):
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "HW1Q953296669L2D"
    proxyPass = "822B0A8AC3A7CA2D"

    def __init__(self):
        super().__init__(self.proxyHost, self.proxyPort, self.proxyUser, self.proxyPass)
