from apitestbasic import GraphqlApi, GraphqlApiExtension
from Schema import Query, Mutation, PermissionTreeFilterInput, IDInput, CompanyAdminPermissionInput, RoleFilterInput
from support.common_object.tree_object import TreeObjectList, TreeObject
from support import return_id_input, admin
# from .CompanyApi import TypeCompanies
from Apis.PlatformBaseApi.CompanyApi import TypeCompanies
import json


class PermissionObject(TreeObject):
    child_field = "child"
    parent_field = "parent_id"


class PermissionsTreeObject(TreeObjectList):
    tree_object = PermissionObject


class SetCompanyAdminPermission(GraphqlApi):
    api = Mutation.set_company_admin_permission

    def set_company_permission(self, company_id, permissions):
        self.run(
            input=CompanyAdminPermissionInput(company=IDInput(id=company_id), permission=return_id_input(permissions)))
        return self.result


class PermissionTree(GraphqlApi):
    api = Query.permission_tree

    def query_company_permissions(self, company_id):
        self.run(filter=PermissionTreeFilterInput(company=IDInput(id=company_id), scope="company"))
        return PermissionsTreeObject(json.loads(self.result.obj))

    def search_permission(self, name, company_id):
        tree = self.query_company_permissions(company_id)
        nodes = tree.select_path("name", name)
        return nodes

    def search_permission_path(self, name, company_id):
        """选中某个权限，返回该节点所有子节点的权限和从根节点到这个节点的所有路线的权限"""
        nodes = self.search_permission(name, company_id)
        nodes.extend(nodes[-1].sub_fields[1:])
        return [i.id for i in nodes]


class RoleList(GraphqlApiExtension.GraphqlQueryListAPi):
    api = Query.role_list

    def query(self, company_id):
        return self.query_full(filter=RoleFilterInput(company=return_id_input(company_id), scope=["COMPANY_ADMIN"]))

    def query_company_permissions(self, company_id):
        self.query(company_id)
        return self.result.data[0].permissions.id.obj


class CompanyPermissionOperator:

    def __init__(self, company_info):
        self.user = admin
        self.info = company_info
        self.permission_api = PermissionTree(self.user)
        self.set_permission = SetCompanyAdminPermission(self.user)
        self.role_list = RoleList(self.user)
        self.permissions = []

    def change_permission(self, *args):
        permissions = set()
        for permission in args:
            r = self.permission_api.search_permission_path(permission, self.info.id)
            permissions = permissions.union(set(r))
        self.permissions = permissions
        self.set_permission.set_company_permission(self.info.id, permissions)
        return self.set_permission.result

    def query_company_permissions(self):
        return self.role_list.query_company_permissions(self.info.id)

    def query(self):
        return self.role_list.query(self.info.id)

if __name__ == '__main__':
    tree_ = PermissionTree(admin).query_company_permissions(61)
    print(tree_)
    print(tree_.select_deep("name", "平台").id)
