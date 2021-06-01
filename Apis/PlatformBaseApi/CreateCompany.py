from apitestbasic import GraphqlApi, GraphqlApiExtension

from Schema import Query, Mutation, CompanyAppsFilter


class TypeCompanies(GraphqlApiExtension.GraphqlQueryListAPi):
    api = Query.type_companies


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


class MyApps(GraphqlApi):
    api = Query.my_apps


class CreateCompany(GraphqlApiExtension.GraphqlOperationAPi):
    api = Mutation.create_company

    def create_company(self, **kwargs):
        params = self.new_var()
        input_ = params.input
        type_id = kwargs.pop("type", None)
        if type_id:
            input_.type.id = type_id
        for key, value in kwargs.items():
            setattr(input_, key, value)
        return self.run()
