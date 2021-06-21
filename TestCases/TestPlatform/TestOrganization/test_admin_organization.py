import allure
import pytest

from Apis.PlatformBaseApi.OrganizationApi import *
from Apis.PlatformBaseApi.CompanyApi import *
from support import admin, run_certain, AssertObj, AssertSearch, record


@allure.feature("组织管理")
class TestAdminOrganization:

    @allure.story("基础信息编辑")
    @allure.title("编辑公司信息")
    def test1(self, company):
        update = UpdateCompany(admin)
        input_ = update.variables.input
        input_.id = company.id.obj
        input_.companyType.id = 2
        input_.province, input_.city, input_.county = CreateCompany(admin).random_address
        record("variables", update.variables)
        update.run()
        company = TypeCompanies(admin).search_company_by_id(company.id)
        AssertObj.assert_true(update.result)
        AssertObj.assert_results(
            update.variables.input,
            company,
            # ("companyType.id", "type.id"),
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
        assert update.variables.input.companyType.id == company.type.id


if __name__ == '__main__':
    run_certain(__file__, "TestAdminOrganization", "test1")
