from apitestbasic import GraphqlApi
from Schema import Query, Mutation, PermissionTreeFilterInput, IDInput, CompanyAdminPermissionInput
from support.common_object.tree_object import TreeObjectList, TreeObject
import json


class Permission(TreeObject):
    child_field = "child"


class PermissionsTree(TreeObjectList):
    tree_object = Permission


class SetCompanyAdminPermission(GraphqlApi):
    api = Mutation.set_company_admin_permission

    def set_company_permission(self, company_id, permissions):
        self.run(input=CompanyAdminPermissionInput(company=IDInput(id=company_id), permission=permissions))
        return self.result


class PermissionTree(GraphqlApi):
    api = Query.permission_tree

    def search(self, name, company_id, scope="company"):
        self.run(filter=PermissionTreeFilterInput(company=IDInput(id=company_id), scope=scope))
        tree = PermissionsTree(json.loads(self.result.obj))
        return tree.select("name", name)


if __name__ == '__main__':
    from support.user import User

    p = PermissionTree(User("admin", "teletraan"))
    p.run(filter=PermissionTreeFilterInput(company=IDInput(id=24), scope="company"))
    tree = PermissionsTree(json.loads(p.result.obj))
    t = tree.select_path("name", "主设备管理")


    def print_name(t_list):
        for i in t_list:
            print(i.id, i.name)


    print_name(t)

    print_name(t[-1].sub_fields)
