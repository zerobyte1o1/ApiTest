from apitestbasic import GraphqlApi, GraphqlApiExtension
from support import search_result, QueryAllApi, random_choice, create_str, return_id_input

from Schema import Query, Mutation, CompanyAppsFilter, MyAppListFilter, AddCompanyAppsInput, companyExistsFilter, \
    CompanyAdminUsersFilter, ResetPasswordInput, DeleteCompanyAdminUsersInput


class TypeCompanies(QueryAllApi):
    api = Query.type_companies

    def search_company_by_type(self, type_id, name):
        self.run()
        type_results = search_result(self.result.data, "type.id", type_id)
        return search_result(type_results.companies, "name", name)

    def search_company_by_name(self, name):
        self.run()
        return search_result(self.result.data.companies, "name", name)


class Provinces(GraphqlApi):
    api = Query.provinces


class Cities(GraphqlApi):
    api = Query.cities

    def cities(self, province_id):
        return self.run(province_id=province_id)


class Counties(GraphqlApi):
    api = Query.counties

    def counties(self, city_id):
        return self.run(city_id=city_id)


class CompanyTypeList(GraphqlApiExtension.GraphqlQueryListAPi):
    api = Query.company_type_list


class CompanyApps(GraphqlApiExtension.GraphqlQueryListAPi):
    api = Query.company_apps

    def query_company_apps(self, company_id):
        return self.query(filter=CompanyAppsFilter(company_id=company_id))


class MyAppList(GraphqlApiExtension.GraphqlQueryListAPi):
    api = Query.my_app_list

    def query_omit_apps(self, company_id):
        """超级管理员查询企业未订阅的app列表"""
        return self.query(filter=MyAppListFilter(company=return_id_input(company_id)))

    def query_my_apps(self):
        """企业管理员调用查询自己公司有的app"""
        return self.query()


class AddCompanyApps(GraphqlApi):
    api = Mutation.add_company_apps

    def add(self, company_id, app_ids: list):
        return self.run(input=AddCompanyAppsInput(company_id=company_id, app_ids=app_ids))


class CompanyExist(GraphqlApi):
    api = Query.company_exists

    def exist(self, **kwargs):
        return self.run(filter=companyExistsFilter(**kwargs))


class CreateCompany(GraphqlApiExtension.GraphqlOperationAPi):
    api = Mutation.create_company

    @property
    def random_type(self):
        return random_choice(CompanyTypeList(self.user).run().result.data.id)

    @property
    def random_address(self):
        province = random_choice(Provinces(self.user).run().result)
        city = random_choice(Cities(self.user).cities(province.id).result)
        county = random_choice(Counties(self.user).counties(city.id).result)
        return province.name, city.name, county.name

    def normal_request(self, name=None):
        input_ = self.variables.input
        # input_.stay("name", "type", "province", "city", "county")
        if name:
            input_.name = name
        input_.type.id = self.random_type
        input_.province, input_.city, input_.county = self.random_address
        self.run()
        return TypeCompanies(self.user).search_company_by_type(input_.type.id, input_.name)


class DeleteCompanies(GraphqlApiExtension.GraphqlOperationAPi):
    api = Mutation.delete_companies

    def delete(self, ids: list):
        self.variables.input.ids = ids
        self.run()
        return self.result


#  企业管理员用户接口
class AccountExists(GraphqlApi):
    api = Query.account_exists

    def exist(self, account):
        return self.run(account=account)


class CompanyAdminUsers(GraphqlApiExtension.GraphqlQueryListAPi):
    api = Query.company_admin_users

    def query_company_admin(self, company_id):
        return self.query_full(filter=CompanyAdminUsersFilter(company_ids=[company_id]))

    def search_admin(self, company_id, account):
        self.query_company_admin(company_id)
        return search_result(self.result.data, "account", account)


class CreateCompanyAdminUser(GraphqlApiExtension.GraphqlOperationAPi):
    api = Mutation.create_company_admin_user

    @property
    def random_company(self):
        return random_choice(TypeCompanies(self.user).run().result_.data[0].companies).id

    def normal_request(self, company_id=None):
        account = create_str("account_")
        if not company_id:
            company_id = self.random_company
        input_ = self.variables.input
        input_.account = account
        input_.company.id = company_id
        self.run()
        return CompanyAdminUsers(self.user).search_admin(company_id, account)


class UpdateCompanyAdminUser(GraphqlApiExtension.GraphqlOperationAPi):
    api = Mutation.update_company_admin_user


class ResetPassword(GraphqlApi):
    api = Mutation.reset_password

    def reset_password(self, user_id):
        return self.run(input=ResetPasswordInput(user_ids=[user_id]))


class DeleteCompanyAdminUsers(GraphqlApi):
    api = Mutation.delete_company_admin_users

    def delete(self, user_id):
        return self.run(input=DeleteCompanyAdminUsersInput(ids=[user_id]))


if __name__ == '__main__':
    from support import admin

    print(UpdateCompanyAdminUser(admin).variables)
