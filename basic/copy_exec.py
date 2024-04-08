import copy

if __name__ == "__main__":
    # 浅拷贝示例
    a = [[1, 2, 3], [4, 5, 6]]
    b = copy.copy(a)
    b[0][0] = 100
    print(a)  # Output: [[100, 2, 3], [4, 5, 6]]
    # 深拷贝示例
    a = [[1, 2, 3], [4, 5, 6]]
    b = copy.deepcopy(a)
    b[0][0] = 100
    print(a)  # Output: [[1, 2, 3], [4, 5, 6]]