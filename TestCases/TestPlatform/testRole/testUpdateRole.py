from Apis.PlatformBaseApi.RoleApi import *
import allure
from support import  AssertObj


class TestUpdateRole:
    @allure.title('更新角色')
    def test(self):
        update=UpdateRole(admin)
        update.update_role(companyid=36,id=188,desc='备注',name="角色3",permissionid="811")
        update.run()
        AssertObj.assert_true(update.result)


if __name__ == '__main__':
    from support import run

    run(__file__)
