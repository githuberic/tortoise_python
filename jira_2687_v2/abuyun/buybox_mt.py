import random
import threading

from multiprocessing.dummy import Pool as ThreadPool

from jira_2687_v2.utils.http_util import HttpUtil
from jira_2687_v2.utils.amazon_buybox_parser_util import AmazonBuyBoxParserUtil
from jira_2687_v2.abuyun.logging_util import LoggingUtil
from jira_2687_v2.utils.file_util import FileUtil

index = 0
success_count = 0
failure_count = 0
retry_count = 0

lock = threading.Lock()

BIZ_CODE = "abuyun"


def get_proxy():
    # 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "HW1Q953296669L2D"
    proxyPass = "822B0A8AC3A7CA2D"

    url_proxy = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }

    proxy_handler = {'http': url_proxy, 'https': url_proxy}

    return proxy_handler


def main_starter(arr_asin, arr_cookie):
    global success_count, failure_count, index, retry_count

    dict_asin_retry = {}
    for asin in arr_asin:
        asin = asin.replace("\"", "").strip()
        dict_asin_retry[asin] = 0

        # Amazon url
        url_amazon = f"https://www.amazon.com/dp/{asin}?th=1&psc=1"

        # amazon url header
        cookie = random.choice(arr_cookie)
        headers_amazon = HttpUtil.get_amz_pd_req_url_header(cookie,asin)

        # 购物车文本
        btn_buybox_text = None
        # 每个 cookie 最多重试3次
        retry_count = 0
        sucss_cur_thread = False
        file_path = ""
        while retry_count < 3:
            # 请求amazon
            response_text = HttpUtil.send_request(url_amazon, headers=headers_amazon, proxy=get_proxy(), timeout=60)
            with lock:
                if response_text is not None:
                    # 原始文件保存
                    file_path = FileUtil.write_content_to_file(BIZ_CODE,asin, response_text)
                    try:
                        # 解析amazon页面
                        btn_buybox_text = AmazonBuyBoxParserUtil.parse_amazon_product_detail_buybox(response_text);
                        if btn_buybox_text is not None:
                            success_count += 1
                            sucss_cur_thread = True
                        else:
                            failure_count += 1
                            retry_count += 1
                            dict_asin_retry[asin] += 1
                    except Exception as e:
                        failure_count += 1
                        dict_asin_retry[asin] += 1
                        LoggingUtil.write_log_to_file(BIZ_CODE, f"Parse_amazon_page error: {e}")
                else:
                    failure_count += 1
                    retry_count += 1
                    dict_asin_retry[asin] += 1

                index += 1

                if dict_asin_retry[asin] > 5:
                    LoggingUtil.write_log_to_file(BIZ_CODE, f"Asin={asin},重试次数超过5次")
                    break

                # 实时记录日志
                thread_id = threading.current_thread().ident
                log_cur = f"Asin = {asin},thread = {thread_id},index = {index},success = {success_count},failure = {failure_count}, retry_count = {retry_count}, buybox = {btn_buybox_text},\n\rfile={file_path}"
                LoggingUtil.write_log_to_file(BIZ_CODE, log_cur)

                if sucss_cur_thread is True:
                    break
        else:
            arr_cookie.remove(cookie)


def main():
    path_products = "../resources/products.txt"
    path_cookies = "../resources/US_90001.cookie"

    arr_products = FileUtil.read_file_split_line_ret_arr(path_products)
    arr_cookies = FileUtil.read_file_split_line_ret_arr(path_cookies)

    print(f"{len(arr_products)}>>>")
    print(f"{len(arr_cookies)}>>>")

    # 设定要启用的线程数量
    num_threads = 5

    # 分割数组成多个子数组
    sub_products_arr = [arr_products[i:i + 10000] for i in range(0, len(arr_products), 10000)]
    sub_cookie_arr = [arr_cookies[i:i + 2000] for i in range(0, len(arr_cookies), 2000)]

    # 创建线程池并指定线程数
    with ThreadPool(5) as pool:
        # 提交任务给线程池处理
        pool.starmap(main_starter, [(sub_products_arr[0], sub_cookie_arr[0]), (sub_products_arr[1], sub_cookie_arr[0]),
                                    (sub_products_arr[2], sub_cookie_arr[1]), (sub_products_arr[3], sub_cookie_arr[1]),
                                    (sub_products_arr[4], sub_cookie_arr[2]), (sub_products_arr[5], sub_cookie_arr[2]),
                                    (sub_products_arr[6], sub_cookie_arr[3]), (sub_products_arr[7], sub_cookie_arr[3]),
                                    (sub_products_arr[8], sub_cookie_arr[4]), (sub_products_arr[9], sub_cookie_arr[4])])
        # pool.close()
        # pool.join()


if __name__ == "__main__":
    LoggingUtil.write_log_to_file(BIZ_CODE, content=">>>阿布云(购物车)-多线程")
    main()
