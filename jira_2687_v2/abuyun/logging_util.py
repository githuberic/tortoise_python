import time
from datetime import datetime

class LoggingUtil:
    def __init__(self):
        pass

    @staticmethod
    def write_log_to_file(biz_code, content):
        file_path = f"{biz_code}_buybox_mt_log.txt"
        with open(file_path, "a") as file:
            file.write(LoggingUtil._wirte_log_append_time(content) + "\n")

    @staticmethod
    def _get_cur_time():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _wirte_log_append_time(content):
        return f"Time:{LoggingUtil._get_cur_time()}\t{content}"
