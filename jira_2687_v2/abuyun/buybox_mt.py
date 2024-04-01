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

index = 0
success_count = 0
failure_count = 0
retry_count = 0

lock = threading.Lock()


def scrape(asin, cookie, stat, proxy_handler):
    # Amazon url
    url_amazon = URLUtil.get_product_detail_url(asin)
    # amazon http-header
    headers_amazon = HttpUtil.get_amz_pd_req_url_header(cookie, asin)
    response_text = HttpClient.send_request(url_amazon, headers=headers_amazon, proxy=proxy_handler, timeout=60)
    # 总数+1
    stat.incr_index()

    if response_text is not None:
        # 原始文件保存
        file_path = FileUtil.write_content_to_file(Constants.ABUYUN, asin, response_text)
        try:
            # 解析amazon页面
            btn_buybox_text = BuyBoxParserUtil.parse_amazon_product_detail_buybox(response_text);
            if btn_buybox_text is not None:
                stat.incr_success_count()
                # sucss_cur_thread = True
            else:
                stat.incr_fail_count()
                # retry_count += 1
                dict_asin_retry[asin] += 1
        except Exception as e:
            stat.incr_fail_count()
            dict_asin_retry[asin] += 1
            LoggingUtil.write_log_to_file(Constants.ABUYUN, f"Parse_amazon_page error: {e}")

        # 异步解析执行
        t = threading.Thread(target=async_parser, args={asin, response_text, stat})
        t.start()
        t.join()

    else:
        stat.incr_fail_count()
        # retry_count += 1
        # dict_asin_retry[asin] += 1


def async_parser(asin, res_content, stat):
    file_path = FileUtil.write_content_to_file(Constants.ABUYUN, asin, res_content)
    btn_buybox_text = BuyBoxParserUtil.parse_amazon_product_detail_buybox(res_content)
    if btn_buybox_text is not None:
        stat.incr_success_count()
    else:
        stat.incr_fail_count()


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
        pool.starmap(main_starter, [(sub_products_arr[0], sub_cookie_arr[0], proxy_handler),
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
