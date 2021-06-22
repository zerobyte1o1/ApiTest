import allure
import pytest
from collections.abc import Callable

from Apis.PlatformBaseApi.OrganizationApi import *
from Apis.PlatformBaseApi.CompanyApi import *
from support import admin, run_certain, AssertObj, record, SendRequestError


@pytest.fixture(scope="function")
def operator(company):
    return DepartmentOperator(admin, company.id)


@allure.feature("组织管理")
class TestAdminOrganization:

    @allure.story("基础信息编辑")
    @allure.title("编辑公司信息")
    @pytest.mark.last
    @pytest.mark.parametrize("method", [Company(admin).query, TypeCompanies(admin).search_company_by_id],
                             ids=["使用typeCompanies查询", "使用company查询"])
    def test1(self, company, method: Callable):
        update = UpdateCompany(admin)
        input_ = update.variables.input
        input_.id = company.id.obj
        input_.companyType.id = 2
        input_.province, input_.city, input_.county = CreateCompany(admin).random_address
        record("variables", update.variables)
        update.run()
        company = method(company.id)
        AssertObj.assert_true(update.result)
        AssertObj.assert_results(
            update.variables.input,
            company,
            ("companyType.id", "type.id"),
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

    @allure.story("组织信息")
    @allure.title("查询公司根节点组织信息")
    def test2(self, company):
        operator = DepartmentOperator(admin, company.id)
        assert operator.root.name == company.name

    @allure.story("组织信息")
    @allure.title("创建子组织节点")
    def test3(self, company, operator):
        name1 = "1级子节点"
        name2 = "2级子节点"
        operator.create.create(name1, operator.root)
        node1 = operator.search_node(".".join([company.name.obj, name1]))
        assert node1
        operator.create.create(name2, node1)
        node2 = operator.search_node(".".join([company.name.obj, name1, name2]))
        assert node2

    @allure.story("组织信息")
    @allure.title("查询是否有重名节点")
    def test4(self, organization_nodes, operator):
        node1, node2 = organization_nodes
        root = operator.root
        with allure.step("存在名字为 {node1.name} 和 {node2.name} 的节点"):
            with allure.step("发送接口parentid为根节点，name为{node1.name},返回True"):
                AssertObj.assert_true(operator.assert_department.query_create(root, node1.name).result)
            with allure.step("发送接口parentid为根节点，name为{node1.name},返回True"):
                AssertObj.assert_false(operator.assert_department.query_create(root).result)
            with allure.step("发送接口parentid为根节点，name为{node1.name}，id为{node1.name}, 返回false"):
                AssertObj.assert_false(
                    operator.assert_department.query_update(node1, root, node1.name).result
                )
            with allure.step("发送接口parentid为根节点，name为{node1.name},id为{node2.name}，返回true"):
                AssertObj.assert_true(
                    operator.assert_department.query_update(node1, root, node2.name).result
                )

    @allure.story("组织信息")
    @allure.title("更新节点名称")
    def test5(self, company, organization_node, operator):
        name = create_str("修改后的名称")
        u = UpdateDepartment(admin).update_name(organization_node, name)
        AssertObj.assert_true(u)
        node = operator.search_node(".".join([company.name.obj, name]))
        assert node

    @allure.story("组织信息")
    @allure.title("更新节点位置")
    def test6(self, company, organization_nodes, operator):
        node1, node2 = organization_nodes
        u = UpdateDepartment(admin).update_position(node1, node2, node1.name)
        AssertObj.assert_true(u)
        node = operator.search_node(".".join([company.name.obj, node2.name, node1.name]))
        assert node

    @allure.story("组织信息")
    @allure.title("更新节点位置失败--存在重名节点")
    def test7(self, company, organization_nodes, operator):
        node1, node2 = organization_nodes
        CreateDepartment(admin).create(node1.name, node2)
        with pytest.raises(SendRequestError):
            u = UpdateDepartment(admin).update_position(node1, node2, node1.name)

    @allure.story("组织信息")
    @allure.title("删除节点")
    def test8(self, organization_node, operator):
        """待开发"""
        # with allure.step("当有人员关联部门不让删除"):
        #     with pytest.raises(SendRequestError):
        #         operator.delete.delete(organization_node)
        with allure.step("当没有人员关联部门时可以删除"):
            operator.delete.delete(organization_node)


if __name__ == '__main__':
    run_certain(__file__, "TestAdminOrganization", is_clear=True)
