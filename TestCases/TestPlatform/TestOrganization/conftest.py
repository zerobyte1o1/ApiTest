from Apis.PlatformBaseApi.CompanyApi import *
from Apis.PlatformBaseApi.PermissionsApi import CompanyPermissionOperator
from Apis.PlatformBaseApi.OrganizationApi import DepartmentOperator
import pytest
from support import User, admin


@pytest.fixture(scope="module")
def company():
    c = CreateCompany(admin)
    company = c.normal_request(create_str("company"))
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


@pytest.fixture(scope="function")
def organization_nodes(company):
    operator = DepartmentOperator(admin, company.id)
    root = operator.root
    name1 = create_str("造数据-1级子节点1")
    name2 = create_str("造数据-1级子节点2")
    operator.create.create(name1, root)
    node1 = operator.search_node(".".join([company.name.obj, name1]))
    operator.create.create(name2, root)
    node2 = operator.search_node(".".join([company.name.obj, name2]))
    return node1, node2


@pytest.fixture(scope="function")
def organization_node(company):
    operator = DepartmentOperator(admin, company.id)
    root = operator.root
    name = create_str("造数据用")
    operator.create.create(name, root)
    node = operator.search_node(".".join([company.name.obj, name]))
    return node
