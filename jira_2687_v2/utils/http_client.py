import requests

class HttpClient:

    def __init__(self):
        pass

    @staticmethod
    def send_request(url, headers=None, proxy=None, timeout=None):
        try:
            response = requests.get(url, headers=headers, proxies=proxy, timeout=timeout)
            return response.text
        except requests.exceptions.RequestException as e:
            error_message = f"Error : {e} \t Proxy: {proxy}"
            raise (error_message)
            return None