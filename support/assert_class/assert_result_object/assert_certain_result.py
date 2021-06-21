from jsonpath import jsonpath


class AssertJsonpath:

    @classmethod
    def assert_jsonpath_result(cls, variables, data, json_path1, json_path2=None):
        """校验api中的结果和参数一致"""
        json_path1 = '$..' + json_path1
        json_path2 = "$.." + json_path2
        value1 = jsonpath(variables.obj, json_path1)
        if json_path2:
            value2 = jsonpath(variables.obj, json_path2)
        else:
            value2 = jsonpath(data, json_path1)
        assert value1 == value2

    @classmethod
    def assert_jsonpath_results(cls, variables, data, *args):
        """校验api中的结果和参数一致,每个args代表jsonpath，会比较参数和结果的jsonpath"""
        for i in args:
            if isinstance(i, tuple):  # 如果是tuple，参数和返回结果使用不一样的jsonpath
                cls.assert_jsonpath_result(variables, data, i[0], i[1])
            else:
                cls.assert_jsonpath_result(variables, data, i)

    @classmethod
    def assert_no_error(cls, api):
        """校验结果中有错误"""
        regex = '$..errors'
        assert not jsonpath(api.data, regex)

    @classmethod
    def assert_has_error(cls, api):
        """校验结果中没有错误"""
        regex = '$..errors'
        assert jsonpath(api.data, regex)

    @classmethod
    def assert_result(cls, api, json_path, value):
        result = jsonpath(api.data, json_path)
        assert result == value


class AssertObj:
    @classmethod
    def get_path(cls, obj, path: str):
        names = path.split(".")
        for name in names:
            obj = getattr(obj, name)
        return obj

    @classmethod
    def assert_result(cls, variables, obj, path):
        assert cls.get_path(variables, path) == cls.get_path(obj, path)

    @classmethod
    def assert_results(cls, variables, obj, *args):
        for path in args:
            assert cls.get_path(variables, path) == cls.get_path(obj, path)

    @classmethod
    def assert_true(cls, result):
        assert result.obj is True

    @classmethod
    def assert_false(cls, result):
        assert result.obj is False


class AssertSearch:

    @classmethod
    def assert_search_result(cls, method, name):
        assert method(name)

    @classmethod
    def assert_search_results(cls, method, *name):
        for i in name:
            cls.assert_search_result(method, i)

    @classmethod
    def assert_not_search_result(cls, method, name):
        assert not method(name)

    @classmethod
    def assert_not_search_results(cls, method, *name):
        for i in name:
            cls.assert_not_search_result(method, i)

    @classmethod
    def assert_list_contains(cls, a, b):
        for i in b:
            assert i in a

    @classmethod
    def assert_list_equal(cls, a, b):
        cls.assert_list_contains(a, b)
        cls.assert_list_contains(b, a)
