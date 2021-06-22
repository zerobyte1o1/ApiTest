import json
from .PermissionsApi import RoleList, PermissionTree, PermissionsTreeObject
from apitestbasic import GraphqlApi, GraphqlApiExtension
from Schema import Mutation, PermissionTreeFilterInput, IDInput, PermissionInput
from support import admin, create_str, search_result


class CreateRole(GraphqlApiExtension.GraphqlOperationAPi):
    api = Mutation.create_role


class UpdateRole(GraphqlApiExtension.GraphqlOperationAPi):
    api = Mutation.update_role


class DeleteRole(GraphqlApi):
    api = Mutation.delete_role

    def delete(self, id_):
        return self.run(id=id_)


class AdminCompanyPermissionTree(PermissionTree):
    def query_company_permissions(self, company_id):
        assert company_id
        self.run(filter=PermissionTreeFilterInput(company=IDInput(id=company_id), scope="role"))
        return PermissionsTreeObject(json.loads(self.result.obj))


class CompanyPermissionTree(PermissionTree):
    def query_company_permissions(self, company_id=None):
        self.run(filter=PermissionTreeFilterInput(scope="role"))
        return PermissionsTreeObject(json.loads(self.result.obj))


def return_permission_input(permissions, permissions_info):
    """赋予permission数据权限"""
    result = []
    for permission in permissions:
        if permission.name in permissions_info.keys():
            data_range = permissions_info[permission.name]
        else:
            data_range = "ALL"
        result.append(
            PermissionInput(permission=IDInput(id=permission.id),
                            data_range=data_range))
    return result


class AdminRoleOperator:
    user = admin

    def __init__(self, company):
        self.create = CreateRole(self.user)
        self.update = UpdateRole(self.user)
        self.delete = DeleteRole(self.user)
        self.role_list = RoleList(self.user)
        self.permission_api = AdminCompanyPermissionTree(self.user)
        self.company = company

    def set_permission_info(self, permission_info):
        permissions = set()
        for permission in permission_info.keys():
            r = self.permission_api.search_permission_nodes(permission, self.company.id)
            permissions = permissions.union(set(r))
        permissions = permissions
        self.create.variables.input.permissions = return_permission_input(permissions, permission_info)

    def create_role(self, permission_info: dict, name=None):
        c = self.create
        c.new_var()
        # role名称
        if not name:
            name = create_str("role_name")
        input_ = c.variables.input_
        input_.company.id = self.company.id
        input_.name = name
        # 设置权限
        self.set_permission_info(permission_info)
        self.create.run()
        return search_result(self.role_list.query_company_roles(self.company.id).result.data, "name", name)


class CompanyRoleOperator:

    def __init__(self, user):
        self.user = user
        self.create = CreateRole(self.user)
        self.update = UpdateRole(self.user)
        self.delete = DeleteRole(self.user)
        self.role_list = RoleList(self.user)
        self.permission_api = CompanyPermissionTree(self.user)

    def set_permission_info(self, permission_info):
        """企业管理员操作不传company"_id"""
        permissions = set()
        for permission in permission_info.keys():
            r = self.permission_api.search_permission_nodes(permission)
            permissions = permissions.union(set(r))
        permissions = permissions
        self.create.variables.input.permissions = return_permission_input(permissions, permission_info)

    def create_role(self, permission_info: dict, name=None):
        c = self.create
        c.new_var()
        if not name:
            name = create_str("role_name")
        input_ = c.variables.input_
        # 企业管理员操作不传company"_id
        input_.pop("company")
        input_.name = name
        # 设置权限
        self.set_permission_info(permission_info)
        self.create.run()
        return search_result(self.role_list.query_my_company_roles().result.data, "name", name)
