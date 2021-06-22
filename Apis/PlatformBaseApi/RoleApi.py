from apitestbasic import GraphqlApi, GraphqlApiExtension

from Schema import Query, Mutation, RoleFilterInput
from support import admin, return_id_input


# 查寻角色列表
class RoleList(GraphqlApiExtension.GraphqlQueryListAPi):
    api = Query.role_list

    def rolelist(self, company):
        return self.query_full(filter=RoleFilterInput(company=company, scope=["COMPANY_ADMIN"]))


# 单独查询角色
class RoleSearch(GraphqlApiExtension.GraphqlQueryListAPi):
    api = Query.role_list

    def rolelist(self, company, search):
        return self.query_full(filter=RoleFilterInput(company=company, search=search))


# 创建角色
class CreateRole(GraphqlApiExtension.GraphqlOperationAPi):
    api = Mutation.create_role

    def create_role(self, **kwargs):
        params = self.new_var()
        input_ = params.input
        input_.company.id = kwargs['companyid']
        input_.name = kwargs['name']
        input_.desc = kwargs['desc']
        input_.permissions = [{"permission": {"id": f"{kwargs['permision']}"}}]
        return self.run()


# 删除角色
class DeleteRole(GraphqlApi):
    api = Mutation.delete_role

    def deletrole(self, id):
        return self.run(id=id)

#修改角色
class UpdateRole(GraphqlApiExtension.GraphqlUpdateAPi):
    api=Mutation.update_role
    def update_role(self,**kwargs):
        params=self.new_var()
        input_=params.input
        input_.company.id=kwargs['companyid']
        input_.id=kwargs['id']
        input_.desc=kwargs['desc']
        input_.permissions=[{'permission':{'id':kwargs['permissionid']}}]
        input_.name=kwargs['name']



if __name__ == '__main__':
    # createRole(admin).create_role()
    # a = RoleList(admin).rolelist({"id":"36"}).result
    #
    # print(a)
    # a=RoleSearch(admin).rolelist({"id": "36"},"新").result.data[0].id
    # print(a)
    a=UpdateRole(admin)
    a.update_role(companyid=36,id=188,desc='备注',name="角色3",permissionid="811")
    a.run()
    print(a.result)