from Apis.PlatformBaseApi.RoleApi import *
import allure
import random
from support import assert_true

class TestDeleteRole:
    allure.title("删除角色")
    def test1(self,admin):
        assert deleteRole(admin).deletrole(185).result


if __name__ == '__main__':
    from support import run
    run(__file__)