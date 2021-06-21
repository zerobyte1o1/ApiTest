from Apis.PlatformBaseApi.CompanyApi import *
import allure
from support import AssertJsonpath, AssertObj, admin, create_str, filter_result
import pytest


@pytest.fixture(scope="class")
def new_company():
    c = CreateCompany(admin)
    company = c.normal_request(create_str("api_test_company_"))
    yield company
    DeleteCompanies(admin).delete([company.id])


@allure.feature("企业管理")
class TestCompanyApps:

    @allure.story("企业信息")
    @allure.title("查询企业app")
    def test1(self, new_company):
        apps = CompanyApps(admin).query_company_apps(new_company.id)
        AssertJsonpath.assert_no_error(apps)

    @allure.story("企业信息")
    @allure.title("查询企业没被分配的app列表")
    def test2(self, new_company):
        apps = MyAppList(admin).query_omit_apps(new_company.id)
        AssertJsonpath.assert_no_error(apps)

    @allure.story("企业信息")
    @allure.title("分配企业app")
    def test3(self, new_company):
        with allure.step("新增企业app"):
            app = MyAppList(admin).query_omit_apps(new_company.id).result.data[0]
            add = AddCompanyApps(admin).add(new_company.id, [app.id])
            AssertJsonpath.assert_no_error(add)
        with allure.step("查询企业app"):
            apps = CompanyApps(admin).query_company_apps(new_company.id).result.data
            assert filter_result(apps, "id", app.id)
        with allure.step("查询企业没有的app"):
            apps = MyAppList(admin).query_omit_apps(new_company.id).result.data
            assert not filter_result(apps, "id", app.id)


if __name__ == '__main__':
    from support import run_certain

    run_certain(__file__, "TestCompanyApps", "test3")
