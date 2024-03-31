from fake_useragent import UserAgent
import random
import requests

class HttpUtil:
    def __init__(self):
        pass
    @staticmethod
    def get_amz_pd_req_url_header(cookie, asin):
        # cookie = cookie.replace("lc-main=en_US","lc-main=zh_CN")

        # 自定义Headers for amazon
        headers_amazon = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': f"{cookie}",
            'device-memory': '8',
            'downlink': '1.3',
            'dpr': '1.8',
            'ect': '3g',
            'rtt': '500',
            'sec-ch-device-memory': '8',
            'sec-ch-dpr': '1.8',
            'sec-ch-ua': 'Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-ch-viewport-width': '1600',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'sec-gpc': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'viewport-width': '1600'
        }

        # 自定义user-agent
        headers_amazon["user-agent"] = UserAgent().random

        # 可选的语言列表
        languages = ["en-US", "en-GB", "fr-FR", "es-ES", "de-DE"]
        accept_language = random.choice(languages)
        headers_amazon["accept-language"] = f"zh-CN,zh;q=0.9,{accept_language};q=0.8,en;q=0.7"

        # Refer 设置
        headers_amazon["referer"] = f"https://www.amazon.com/dp/{asin}?th=1&psc=1"

        headers_amazon["accept-encoding"] = "gzip, deflate, br"
        headers_amazon["upgrade-insecure-requests"] = "1"

        return headers_amazon

    @staticmethod
    def send_request(url, headers=None, proxy=None, timeout=None):
        try:
            response = requests.get(url, headers=headers, proxies=proxy, timeout=timeout)
            return response.text
        except requests.exceptions.RequestException as e:
            error_message = f"Error : {e} \t Proxy: {proxy}"
            raise (error_message)
            return None