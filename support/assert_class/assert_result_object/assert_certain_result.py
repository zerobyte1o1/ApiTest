from jsonpath import jsonpath


def assert_api_result(api, json_path1, json_path2=None):
    """校验api中的结果和参数一致"""
    json_path1 = '$..' + json_path1
    json_path2 = "$.." + json_path2
    value1 = jsonpath(api.variables, json_path1)
    if json_path2:
        value2 = jsonpath(api.variables.obj, json_path2)
    else:
        value2 = jsonpath(api.result.obj, json_path1)
    assert value1 == value2


def assert_api_results(api, *args):
    """校验api中的结果和参数一致,每个args代表jsonpath，会比较参数和结果的jsonpath"""
    for i in args:
        if isinstance(i, tuple):  # 如果是tuple，参数和返回结果使用不一样的jsonpath
            assert_api_result(api, i[0], i[1])
        else:
            assert_api_result(api, i)


def assert_no_error(api):
    """校验结果中有错误"""
    regex = '$..errors'
    assert not jsonpath(api.result.obj, regex)


def assert_has_error(api):
    """校验结果中没有错误"""
    regex = '$..errors'
    assert jsonpath(api.result.obj, regex)


def assert_result(api, json_path, value):
    result = jsonpath(api.result.obj, json_path)
    assert result == value
