from Apis.PlatformBaseApi.RoleApi import *
from Apis.PlatformBaseApi.CompanyApi import CompanyTypeList,TypeCompanies
import allure
import random
from support import assert_true

class TestSelectRole:
    @allure.title("查询全部角色")
    def test1(self,admin):
        assert RoleList(admin).run().result




if __name__ == '__main__':
    from support import run

    run(__file__)