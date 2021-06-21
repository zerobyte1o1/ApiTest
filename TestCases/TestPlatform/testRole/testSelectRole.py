from Apis.PlatformBaseApi.RoleApi import *
from Apis.PlatformBaseApi.CompanyApi import CompanyTypeList,TypeCompanies
import allure
import random


class TestSelectRole:
    @allure.title("查询全部角色")
    def test1(self,admin):
        assert RoleList(admin).rolelist("36").run()




if __name__ == '__main__':
    from support import run

    run(__file__)