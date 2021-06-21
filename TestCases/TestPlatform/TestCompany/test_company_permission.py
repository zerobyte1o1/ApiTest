from Apis.PlatformBaseApi.CompanyApi import *
from Apis.PlatformBaseApi.PermissionsApi import *
from functools import partial
import allure
from support import AssertSearch, AssertJsonpath, admin, create_str, load
import pytest


@pytest.fixture(scope="class")
def new_company():
    c = CreateCompany(admin)
    company = c.normal_request(create_str("api_test_company_"))
    yield company
    DeleteCompanies(admin).delete([company.id])


@pytest.fixture(scope="class")
def method(new_company):
    return partial(PermissionTree(admin).search_permission, company_id=new_company.id)


@allure.feature("企业管理")
class TestCompanyPermission:

    @allure.story("企管员菜单权限")
    @allure.title("查询平台权限")
    def test1(self, new_company, method):
        AssertSearch.assert_search_results(
            method,
            *load("data/platform_data/company_platform_menu.yaml")
        )
        AssertSearch.assert_not_search_result(
            method,
            "企业管理"
        )

    @allure.story("企管员菜单权限")
    @allure.title("app侧边栏权限只有为企业添加app才可以看见")
    def test2(self, new_company, method):
        app = MyAppList(admin).query_omit_apps(company_id=new_company.id).result.data[0]
        AssertSearch.assert_not_search_result(
            method,
            app.name
        )
        AddCompanyApps(admin).add(new_company.id, [app.id])
        AssertSearch.assert_search_result(
            method,
            app.name
        )

    @allure.story("企管员菜单权限")
    @allure.title("给企业分配平台侧边栏权限:  {permission}  分配成功")
    @pytest.mark.parametrize("permission", load("data/platform_data/company_platform_menu.yaml"))
    def test3(self, permission, new_company):
        op = CompanyPermissionOperator(new_company)
        with allure.step("更新企业权限"):
            result = op.change_permission(permission)
            AssertJsonpath.assert_no_error(op.set_permission)
        with allure.step("校验查询到的权限是否一致"):
            real_permissions = op.query_company_permissions()
            expect_permissions = op.permissions
            AssertSearch.assert_list_equal(real_permissions, expect_permissions)


if __name__ == '__main__':
    from support import run_certain

    run_certain(__file__, "TestCompanyPermission", "test3")
