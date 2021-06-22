from Apis.PlatformBaseApi.RoleApi import *
from Apis.PlatformBaseApi.CompanyApi import CompanyTypeList, TypeCompanies
import allure
import random


class TestSelectRole:
    @allure.title("查询全部角色")
    def test1(self):
        assert RoleList(admin).rolelist({"id": "36"}).result

    @allure.title("查询部分")
    def test2(self):
        assert RoleSearch(admin).rolelist({"id": "36"},"2").result


if __name__ == '__main__':
    from support import run

    run(__file__)
