from Apis.PlatformBaseApi.CompanyApi import *
import allure
from support import AssertObj, admin, create_str, filter_result
import pytest


@pytest.fixture(scope="function")
def new_company():
    c = CreateCompany(admin)
    company = c.normal_request(create_str("api_test_company_"))
    yield c, company
    DeleteCompanies(admin).delete([company.id])


@allure.feature("企业管理")
class TestCompanyList:

    @allure.story("企业列表")
    @allure.title("查询企业类型和列表")
    def test1(self):
        type_companies = TypeCompanies(admin).run()
        assert type_companies.result

    @allure.story("企业列表")
    @allure.title("查询省份")
    def test2(self):
        assert len(Provinces(admin).run().result.data) == 30

    @allure.story("企业列表")
    @allure.title("查询市")
    def test3(self):
        province_id = "110000000000"  # 北京市
        assert Cities(admin).cities(province_id).result.data[0].name == "市辖区"

    @allure.story("企业列表")
    @allure.title("查询区")
    def test4(self):
        city_id = "110100000000"
        assert len(Counties(admin).counties(city_id).result.data) == 15

    @allure.story("企业列表")
    @allure.title("查询企业类型列表")
    def test5(self):
        assert len(CompanyTypeList(admin).run().result) == 9

    @allure.story("企业列表")
    @allure.title("创建企业")
    def test6(self, new_company):
        c, company = new_company
        input_ = c.variables.input
        AssertObj.assert_true(c.result)
        AssertObj.assert_results(
            input_,
            company,
            "type.id",
            "name",
            "address",
            "uscc",
            "contact",
            "email",
            "phone",
            "province",
            "city",
            "county"
        )

    @allure.story("企业列表")
    @allure.title("删除企业")
    def test7(self, new_company):
        company = new_company[1]
        result = DeleteCompanies(admin).delete([company.id])
        AssertObj.assert_true(result)
        assert not filter_result(TypeCompanies(admin).run().result.data.companies, "id", company.id)

    @allure.story("企业列表")
    @allure.title("companyExist name")
    def test8(self, new_company):
        new_company_name = create_str("api_test_company_")
        a = CompanyExist(admin)
        company = new_company[1]
        with allure.step(f"当{new_company_name}的公司不存在"):
            a.exist(name=new_company_name)
            AssertObj.assert_false(a.result)
        with allure.step(f"当{company.name}的公司存在"):
            a.exist(name=company.name)
            AssertObj.assert_true(a.result)
        with allure.step(f"当{company.name}的公司存在,但是传入该companyid"):
            a.exist(name=company.name, id=company.id)
            AssertObj.assert_false(a.result)

    @allure.story("企业列表")
    @allure.title("companyExist uscc")
    def test9(self, new_company):
        new_uscc_name = create_str("uscc")
        a = CompanyExist(admin)
        company = new_company[1]
        with allure.step(f"当{new_uscc_name}的社会信用代码不存在"):
            a.exist(uscc=new_uscc_name)
            AssertObj.assert_false(a.result)
        with allure.step(f"当{company.name}的社会信用代码存在"):
            a.exist(uscc=company.uscc)
            AssertObj.assert_true(a.result)
        with allure.step(f"当{company.name}的社会信用代码存在,但是传入该companyid"):
            a.exist(uscc=company.uscc, id=company.id)
            AssertObj.assert_false(a.result)


if __name__ == '__main__':
    from support import run_certain

    run_certain(__file__, "TestCompanyList", "test9")
