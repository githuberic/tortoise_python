def start():
    try:
        list = [1, 2, 3]
        print(1 / 0)
    except IndexError as msg:
        print(msg)
    except ZeroDivisionError as msg:
        print(msg)
    else:
        print('Not other exception')
    finally:
        print('Exception>>>')


if __name__ == "__main__":
    start()
