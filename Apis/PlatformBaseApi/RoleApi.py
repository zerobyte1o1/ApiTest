from apitestbasic import GraphqlApi, GraphqlApiExtension

from Schema import Query, Mutation,RoleFilterInput

class RoleList(GraphqlApiExtension.GraphqlQueryListAPi):
    api=Query.role_list


class DeleRole(GraphqlApi):
    api=Mutation.delete_role
    def delerole(self, province_id):
        return self.run(province_id=province_id)

class createRole(GraphqlApi):
    api=Mutation.create_role
    def create_role(self, **kwargs):
        params = self.new_var()
        input_ = params.input
        type_id = kwargs.pop("type", None)
        if type_id:
            input_.type.id = type_id
        for key, value in kwargs.items():
            setattr(input_, key, value)
        return self.run()

class deleteRole(GraphqlApi):
    api=Mutation.delete_role
    def deletrole(self,id):
        return self.run(id)
