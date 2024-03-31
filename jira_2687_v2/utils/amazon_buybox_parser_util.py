from bs4 import BeautifulSoup

class AmazonBuyBoxParserUtil:
    def __init__(self):
        pass

    @staticmethod
    def parse_amazon_product_detail_buybox(res_content):
        btn_text = None

        # 使用BeautifulSoup解析HTML页面
        soup = BeautifulSoup(res_content, 'html.parser')

        # 查找购物车按钮
        btn_buy_now = soup.find('span', id='submit.buy-now-announce')

        btn_add_to_ubb_cart = soup.find('span', id='submit.add-to-cart-ubb-announce')
        btn_add_to_cart = soup.find('span', id='submit.add-to-cart-announce')

        # Set Up Now
        btn_setup_now = soup.find('button', id='rcx-subscribe-submit-button-announce')

        # 提取按钮文本
        if btn_buy_now is not None:
            return btn_buy_now.text.strip()
        elif btn_add_to_cart is not None:
            return btn_add_to_cart.text.strip()
        elif btn_add_to_ubb_cart is not None:
            return btn_add_to_ubb_cart.text.strip()
        elif btn_setup_now is not None:
            return btn_setup_now.text.strip()
        return btn_text