from util_module import UtilClass

# 在其他模块中调用静态方法
if __name__ == "__main__":
    result = UtilClass.my_static_method(23, 2)
    print(result)  # 输出：3
    result = UtilClass.write_log_to_file("abuyun", "start testing>>>")
    print(result)  # 输出：3