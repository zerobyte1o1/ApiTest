from apitestbasic import GraphqlApi, GraphqlApiExtension
from Schema import Query, Mutation, UserListFilter
from support import admin, return_id_input


# 搜索
class Users(GraphqlApiExtension.GraphqlQueryListAPi):
    api = Query.users

    def users(self, search):
        return self.query_full(filter=UserListFilter(search))


# 检查账号是否存在
class AccountExists(GraphqlApi):
    api = Query.account_exists

    def account_exits(self, account):
        return self.run(account=account).result


# 创建用户
class CreateUser(GraphqlApiExtension.GraphqlOperationAPi):
    api = Mutation.create_user

    def create_user(self, **kwargs):
        params = self.new_var()
        input_ = params.input
        input_.account = kwargs['account']
        input_.company.id = kwargs['companyid']
        input_.department.id = kwargs['departmentid']
        input_.desc = kwargs['desc']
        input_.email = kwargs['email']
        input_.isActive = kwargs['isActive']
        input_.name = kwargs['name']
        input_.phone = kwargs['phone']
        input_.role = kwargs['role']
        return self.run()


# 更新用户
class UpdateUser(GraphqlApiExtension.GraphqlUpdateAPi):
    api = Mutation.update_user

    def update_user(self, **kwargs):
        print(self.variables)
        params = self.new_var()
        input_ = params.input
        input_.account = kwargs['account']
        input_.id = kwargs['id']
        input_.department.id = kwargs['departmentid']
        input_.desc = kwargs['desc']
        input_.email = kwargs['email']
        input_.isActive = kwargs['isActive']
        input_.name = kwargs['name']
        input_.phone = kwargs['phone']
        input_.role = kwargs['role']
        return self.run()


# 重置密码
class ResetPassword(GraphqlApiExtension.GraphqlOperationAPi):
    api = Mutation.reset_password

    def reset_password(self, **kwargs):
        self.variables.input.userIDs = [kwargs['userIDs']]
        self.variables.scenario = kwargs['scenario']
        return self.run()


if __name__ == '__main__':
    a = CreateUser(admin).create_user(account='test_user8', companyid='36', departmentid='108',
                                      desc='备注', email='254566451@qq.com', isActive="true",
                                      name='testname2', phone='13457685948', role=[{'id': '188'}]
                                      )
    print(a)
    # a = ResetPassword(admin)
    # a.reset_password(userIDs="63f7bab1-643c-4016-8eeb-cdafd278db20", scenario="NORMAL_USER")
    # print(a.result)
