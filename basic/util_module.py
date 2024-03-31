from datetime import datetime
class UtilClass:
    def __init__(self):
        pass
    @staticmethod
    def my_static_method(param1, param2):
        # 静态方法的实现
        return param1 + param2

    @staticmethod
    def _get_cur_time():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _wirte_log_append_time(content):
        return f"Time:{UtilClass._get_cur_time()}\t{content}"

    @staticmethod
    def write_log_to_file(biz_code, content):
        file_path = f"{biz_code}_{UtilClass._wirte_log_append_time(content)}"
        return file_path