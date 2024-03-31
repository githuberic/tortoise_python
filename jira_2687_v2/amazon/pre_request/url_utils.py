class URLUtil:
    def __init__(self):
        pass

    @staticmethod
    def get_product_detail_url(asin):
        return f"https://www.amazon.com/dp/{asin}?th=1&psc=1"
