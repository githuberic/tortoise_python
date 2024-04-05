import random
import threading

from multiprocessing.dummy import Pool as ThreadPool

from jira_2687_v2.abuyun.http_proxy_abuyun import HttpProxyAbuyun
from jira_2687_v2.utils.http_util import HttpUtil
from jira_2687_v2.utils.http_client import HttpClient
from jira_2687_v2.amazon.post_response.parser.amazon_buybox_parser_util import BuyBoxParserUtil
from jira_2687_v2.abuyun.logging_util import LoggingUtil
from jira_2687_v2.utils.file_util import FileUtil
from jira_2687_v2.amazon.pre_request.url_utils import URLUtil
from jira_2687_v2.stat.atomic_stat import StatAtomic
from jira_2687_v2.stat.request_stat_amazon_pd import RequestStat2AmazonPD
from jira_2687_v2.constants import Constants

index = 0
success_count = 0
failure_count = 0
retry_count = 0

lock = threading.Lock()


class Crawler:
    def __init__(self):
        pass

    def scrape(self, asin, cookie, stat, proxy_handler):
        psd = RequestStat2AmazonPD(asin, cookie)

        # Amazon url
        url_amazon = URLUtil.get_product_detail_url(asin)
        # amazon http-header
        headers_amazon = HttpUtil.get_amz_pd_req_url_header(cookie, asin)
        response_text = HttpClient.send_request(url_amazon, headers=headers_amazon, proxy=proxy_handler, timeout=60)
        # 总数+1
        stat.incr_index()

        pm = BuyBoxParser(asin, response_text, stat, psd)
        pm.async_parser()


class MyException(Exception):
    def __init__(self, err_code="", message="Custom exception occurred"):
        self.err_code = err_code
        super().__init__(message)

    def __str__(self):
        return f"ErrCode={self.err_code},Msg={self.message}"


class ParserManager:
    def __init__(self):
        pass

    def process(self, response_text, stat):
        bReturn = False
        if response_text is not None:
            try:
                # 解析amazon页面
                btn_buybox_text = BuyBoxParserUtil.parse_amazon_product_detail_buybox(response_text);
                if btn_buybox_text is not None:
                    stat.incr_success_count()
                    # sucss_cur_thread = True
                    bReturn = True
                else:
                    stat.incr_fail_count()
                    bReturn = False
                    # retry_count += 1
                    # dict_asin_retry[asin] += 1
            except Exception as e:
                stat.incr_fail_count()
                # dict_asin_retry[asin] += 1
                raise MyException("10001", "Parse_amazon_page error")
                # LoggingUtil.write_log_to_file(Constants.ABUYUN, f"Parse_amazon_page error: {e}")
        else:
            stat.incr_fail_count()

        return bReturn


class BuyBoxParser:
    def __init__(self, asin, res_content, stat, psd):
        self.asin = asin
        self.res_content = res_content
        self.stat = stat
        self.psd = psd

    def _parse_save(self):
        btn_buybox_text = None
        file_path = FileUtil.write_content_to_file(Constants.ABUYUN, self.asin, self.res_content)
        try:
            btn_buybox_text = BuyBoxParserUtil.parse_amazon_product_detail_buybox(self.res_content)
            if btn_buybox_text is not None:
                # 统计_成功次数
                self.stat.incr_success_count()
            else:
                # 统计_失败次数
                self.stat.incr_fail_count()
                # 重试次数
                self.psd.incr_retry_times()
        except Exception as e:
            self.stat.incr_fail_count()
            LoggingUtil.write_log_to_file(Constants.ABUYUN, f"Parse_amazon_page error: {e}")

        # 实时记录日志
        thread_id = threading.current_thread().ident
        log_cur = f"Asin = {self.asin},thread = {thread_id},index = {self.stat.get_index()},success = {self.stat.get_success_count()},failure = {self.stat.get_fail_count()}, retry_count = {self.psd.incr_retry_times()}, buybox = {btn_buybox_text},\n\rfile={file_path}"
        LoggingUtil.write_log_to_file(Constants.ABUYUN, log_cur)

    def async_parser(self):
        if self.res_content is not None:
            t = threading.Thread(target=self._parse_save, args={})
            t.start()
            t.join()
        else:
            # 统计_失败次数
            self.stat.incr_fail_count()
            # 重试次数
            self.psd.incr_retry_times()


def main_starter_v2(arr_asin, arr_cookie, proxy_handler):
    stat = StatAtomic()

    for asin in arr_asin:
        asin = asin.replace("\"", "").strip()
        # amazon url header
        cookie = random.choice(arr_cookie)

        crawler = Crawler()
        crawler.scrape(asin, cookie, stat, proxy_handler)


def main_starter(arr_asin, arr_cookie, proxy_handler):
    global success_count, failure_count, index, retry_count

    stat = StatAtomic()

    dict_asin_retry = {}
    for asin in arr_asin:
        asin = asin.replace("\"", "").strip()
        dict_asin_retry[asin] = 0

        # Amazon url
        url_amazon = URLUtil.get_product_detail_url(asin)

        # amazon url header
        cookie = random.choice(arr_cookie)
        headers_amazon = HttpUtil.get_amz_pd_req_url_header(cookie, asin)

        # 购物车文本
        btn_buybox_text = None
        # 每个 cookie 最多重试3次
        retry_count = 0
        sucss_cur_thread = False
        file_path = ""
        while retry_count < 3:
            # 请求amazon
            response_text = HttpClient.send_request(url_amazon, headers=headers_amazon, proxy=proxy_handler, timeout=60)
            with lock:
                if response_text is not None:
                    # 原始文件保存
                    file_path = FileUtil.write_content_to_file(Constants.ABUYUN, asin, response_text)
                    try:
                        # 解析amazon页面
                        btn_buybox_text = BuyBoxParserUtil.parse_amazon_product_detail_buybox(response_text);
                        if btn_buybox_text is not None:
                            stat.incr_success_count()
                            sucss_cur_thread = True
                        else:
                            stat.incr_fail_count()
                            retry_count += 1
                            dict_asin_retry[asin] += 1
                    except Exception as e:
                        stat.incr_fail_count()
                        dict_asin_retry[asin] += 1
                        LoggingUtil.write_log_to_file(Constants.ABUYUN, f"Parse_amazon_page error: {e}")
                else:
                    stat.incr_fail_count()
                    retry_count += 1
                    dict_asin_retry[asin] += 1

                stat.incr_index()

                if dict_asin_retry[asin] > 5:
                    LoggingUtil.write_log_to_file(Constants.ABUYUN, f"Asin={asin},重试次数超过5次")
                    break

                # 实时记录日志
                thread_id = threading.current_thread().ident
                log_cur = f"Asin = {asin},thread = {thread_id},index = {index},success = {success_count},failure = {failure_count}, retry_count = {retry_count}, buybox = {btn_buybox_text},\n\rfile={file_path}"
                LoggingUtil.write_log_to_file(Constants.ABUYUN, log_cur)

                if sucss_cur_thread is True:
                    break
        else:
            arr_cookie.remove(cookie)


def main():
    path_products = "../resources/products.txt"
    path_cookies = "../resources/US_90001.cookie"

    arr_products = FileUtil.read_file_split_line_ret_arr(path_products)
    arr_cookies = FileUtil.read_file_split_line_ret_arr(path_cookies)

    # 分割数组成多个子数组
    sub_products_arr = [arr_products[i:i + 10000] for i in range(0, len(arr_products), 10000)]
    sub_cookie_arr = [arr_cookies[i:i + 2000] for i in range(0, len(arr_cookies), 2000)]

    # 初始化http代理
    http_proxy = HttpProxyAbuyun()
    proxy_handler = http_proxy.get_proxy()

    # 创建线程池并指定线程数
    with ThreadPool(5) as pool:
        # 提交任务给线程池处理
        pool.starmap(main_starter_v2, [(sub_products_arr[0], sub_cookie_arr[0], proxy_handler),
                                       (sub_products_arr[1], sub_cookie_arr[0], proxy_handler),
                                       (sub_products_arr[2], sub_cookie_arr[1], proxy_handler),
                                       (sub_products_arr[3], sub_cookie_arr[1], proxy_handler),
                                       (sub_products_arr[4], sub_cookie_arr[2], proxy_handler),
                                       (sub_products_arr[5], sub_cookie_arr[2], proxy_handler),
                                       (sub_products_arr[6], sub_cookie_arr[3], proxy_handler),
                                       (sub_products_arr[7], sub_cookie_arr[3], proxy_handler),
                                       (sub_products_arr[8], sub_cookie_arr[4], proxy_handler),
                                       (sub_products_arr[9], sub_cookie_arr[4], proxy_handler)])


if __name__ == "__main__":
    LoggingUtil.write_log_to_file(Constants.ABUYUN, content=">>>阿布云(购物车)-多线程")
    main()
