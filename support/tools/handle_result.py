import random


def filter_result(result: list, name: str, value):
    names = name.split(".")

    def judge(obj):
        r = obj
        for name_ in names:
            r = getattr(r, name_)
        return r == value

    return list(filter(judge, result))


def search_result(search_list: list, name: str, value):
    if isinstance(search_list[0], list):
        new_list = []
        for i in search_list:
            new_list.extend(i)
        search_list = new_list
    result = filter_result(search_list, name, value)
    if result:
        return result[0]
    else:
        raise AssertionError(f"从 {result} 中没找到 {name} 字段为 {value} 的值")


def random_choice(result: list):
    return random.choice(result).obj
