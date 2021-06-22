from Apis.PlatformBaseApi.CompanyApi import *
from Apis.PlatformBaseApi.PermissionsApi import *
from functools import partial
import allure
from support import admin, create_str, AssertObj, AssertJsonpath, run_certain, AssertSearch, \
    filter_result, User
import pytest


@pytest.fixture(scope="class")
def new_company():
    c = CreateCompany(admin)
    company = c.normal_request(create_str("api_test_company_"))
    CompanyPermissionOperator(company).change_permission("平台")
    yield company
    DeleteCompanies(admin).delete([company.id])


@pytest.fixture(scope="function")
def new_company_admin(new_company):
    user = CreateCompanyAdminUser(admin).normal_request(new_company.id)
    yield user
    DeleteCompanyAdminUsers(admin).delete(user.id)


@allure.feature("企业管理")
class TestCompanyAccount:

    @allure.story("用户管理")
    @allure.title("accountExist")
    def test1(self, new_company, new_company_admin):
        fake_name = create_str("account_")
        exist = AccountExists(admin)
        with allure.step("不存在的account"):
            exist.exist(fake_name)
            AssertObj.assert_false(exist.result)
        with allure.step("存在的account"):
            exist.exist(new_company_admin.account)
            AssertObj.assert_true(exist.result)

    @allure.story("用户管理")
    @allure.title("companyAdminUsers查询")
    def test2(self, new_company, new_company_admin):
        users = CompanyAdminUsers(admin).query_company_admin(new_company.id)

        AssertSearch.assert_search_result(
            partial(filter_result, users.result.data, "id"),
            new_company_admin.id
        )

    @allure.story("用户管理")
    @allure.title("创建企业管理员")
    def test3(self, new_company):
        c = CreateCompanyAdminUser(admin)
        user = c.normal_request(new_company.id)
        AssertObj.assert_results(
            c.variables.input,
            user,
            "name",
            "account",
            "phone",
            "email"
        )
        with allure.step("使用密码可以登录"):
            User(user.account, c.result.obj)

    @allure.story("用户管理")
    @allure.title("更新企业管理员")
    def test4(self, new_company, new_company_admin):
        update = UpdateCompanyAdminUser(admin)
        update.variables.input.id = new_company_admin.id
        update.run()
        AssertJsonpath.assert_no_error(update)
        user = CompanyAdminUsers(admin).search_admin(new_company.id, new_company_admin.account)
        AssertObj.assert_results(
            update.variables.input,
            user,
            "name",
            "phone",
            "email"
        )

    @allure.story("用户管理")
    @allure.title("更新用户密码")
    def test5(self, new_company, new_company_admin):
        with allure.step("更新用户密码"):
            reset = ResetPassword(admin).reset_password(new_company_admin.id)
            AssertJsonpath.assert_no_error(reset)
        with allure.step("使用新密码登录"):
            User(new_company_admin.account, reset.result[0].password)

    @allure.story("用户管理")
    @allure.title("删除用户")
    def test5(self, new_company):
        with allure.step("新增用户"):
            c = CreateCompanyAdminUser(admin)
            user = c.normal_request(new_company.id)
        with allure.step("删除用户"):
            d = DeleteCompanyAdminUsers(admin)
            d.delete(user.id)
            AssertObj.assert_true(d.result)
        with allure.step("用户无法登陆"):
            with pytest.raises(Exception) as e:
                User(user.account, c.result.obj)


if __name__ == '__main__':
    run_certain(__file__, "TestCompanyAccount", "test5")
