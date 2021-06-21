from Apis.PlatformBaseApi.CompanyApi import *
from Apis.PlatformBaseApi.PermissionsApi import CompanyPermissionOperator
import pytest
from support import User, admin


@pytest.fixture(scope="module")
def company():
    c = CreateCompany(admin)
    company = c.normal_request(create_str("api_test_company_"))
    CompanyPermissionOperator(company).change_permission("平台")
    yield company
    DeleteCompanies(admin).delete([company.id])


@pytest.fixture(scope="module")
def company_admin_(company):
    c = CreateCompanyAdminUser(admin)
    user = c.normal_request(company.id)
    yield user, User(user.account, c.result.obj)
    DeleteCompanyAdminUsers(admin).delete(user.id)


@pytest.fixture(scope="module")
def company_admin_info(company_admin_):
    return company_admin_[0]


@pytest.fixture(scope="module")
def company_admin_user(company_admin_):
    return company_admin_[1]
