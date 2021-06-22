from Apis.PlatformBaseApi.RoleApi import *
import allure
from support import AssertObj


class TestUpdateRole:

    @classmethod
    def setup_class(cls):
        CreateRole(admin).create_role(companyid=36, name='测试更新角色', desc='备注1', permision=546)
        cls.id = RoleSearch(admin).rolelist({"id": "36"}, "测试更新角色").result.data[0].id

    @classmethod
    def teardown_class(cls):
        DeleteRole(admin).deletrole([cls.id])

    @allure.title('查询角色')
    def test1(self):
        search = RoleSearch(admin).rolelist({"id": "36"}, "测试更新角色").result
        assert search

    @allure.title('更新角色')
    def test2(self):
        update = UpdateRole(admin)
        update.update_role(companyid=36, id=self.id, desc='备注', name="测试更新角色3", permissionid="811")
        AssertObj.assert_true(update.result)


if __name__ == '__main__':
    from support import run

    run(__file__)
