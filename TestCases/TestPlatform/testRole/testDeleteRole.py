from Apis.PlatformBaseApi.RoleApi import *
import allure
from support import AssertObj
import random
import pytest

@pytest.fixture(scope="class")
def new_role():
    CreateRole(admin).create_role(companyid=36,name='删除准备角色',desc='备注1',permision=546)
class TestDeleteRole:
    allure.title("查询角色id")
    def test1(self):
        RoleList(admin).rolelist({"id":"36","search":"删除准备角色"}).result
    allure.title("删除角色")
    def test2(self):
        AssertObj.assert_true(DeleteRole(admin).deletrole(["232"]).result)


if __name__ == '__main__':
    from support import run
    run(__file__)