from Apis.PlatformBaseApi.RoleApi import *
from Apis.PlatformBaseApi.CompanyApi import CompanyTypeList, TypeCompanies
import allure
import random


class TestSelectRole:
    @classmethod
    def setup_class(cls):
        CreateRole(admin).create_role(companyid=36, name='部分查询准备角色', desc='备注1', permision=546)
        cls.id = RoleSearch(admin).rolelist({"id": "36"}, "部分查询准备角色").result.data[0].id
    @classmethod
    def teardown_class(cls):
        DeleteRole(admin).deletrole([cls.id])
    @allure.title("查询全部角色")
    def test1(self):
        assert RoleList(admin).rolelist({"id": "36"}).result

    @allure.title("查询部分")
    def test2(self):
        assert RoleSearch(admin).rolelist({"id": "36"}, "部分查询准备角色").result


if __name__ == '__main__':
    from support import run

    run(__file__)
