import pytest
from Apis.PlatformBaseApi.RoleApi import *
from support import admin, AssertObj
import allure


class TestCreateRole:
    @classmethod
    def teardown_class(cls):
        role = RoleSearch(admin)
        id = role.rolelist({"id": "36"}, "测试角色2").result.data[0].id
        DeleteRole(admin).deletrole([id])

    @allure.title("创建角色")
    def test1(self):
        cr = CreateRole(admin)
        cr.create_role(companyid=36, name='测试角色2', desc='备注1', permision=546)
        AssertObj.assert_true(cr.result)


if __name__ == '__main__':
    from support import run_certain

    run_certain(__file__)
