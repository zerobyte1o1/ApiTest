from functools import wraps


def except_assert_error(exception):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            flag = False
            try:
                result = func(*args, **kwargs)
                flag = True
                return result
            except exception as e:
                print(e)
            finally:
                if flag:
                    raise AssertionError("预期捕获错误，不应该成功")

        return wrapper

    return decorator
