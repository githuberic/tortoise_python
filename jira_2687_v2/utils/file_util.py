import os
import threading
import time
import uuid

class FileUtil:
    def __init__(self):
        pass
    @staticmethod
    def read_file_split_line_ret_arr(file_path):
        if not os.path.exists(file_path):
            return

        lines = []
        with open(file_path, "r") as file:
            for line in file:
                if line.strip() != "":
                    lines.append(line.strip())
        return lines;

    @staticmethod
    def write_content_to_file(biz_code, asin, res_content):
        # asin = url.replace("https://www.amazon.com/dp/","").replace("?th=1","")

        # 获取当前时间的时间戳（以秒为单位）
        timestamp = time.time()
        thread_id = threading.get_ident()
        file_path = f"./amazon/{biz_code}/{asin}/{thread_id}_{uuid.uuid4()}.html"

        # 获取文件所在目录
        directory = os.path.dirname(file_path)
        # 如果目录不存在，则创建它
        if not os.path.exists(directory):
            os.makedirs(directory)

        # 删除已存在的结果文件
        # if os.path.exists(file_path):
        #    os.remove(file_path)

        with open(file_path, "w") as file:
            file.write(res_content)

        return file_path