from Apis.PlatformBaseApi.RoleApi import *
from Apis.PlatformBaseApi.CompanyApi import CompanyTypeList,TypeCompanies
import allure
import random
from support import assert_true

class TestCreateRole:
    @allure.title("创建角色")
    def test1(self,admin):
        cr=createRole(admin)
        cr.create_role(name="testt1",permissions=["1","2"],desc="备注")
        assert_true(cr.result)


if __name__ == '__main__':
    from support import run

    run(__file__)