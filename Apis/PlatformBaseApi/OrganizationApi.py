import json
from apitestbasic import GraphqlApi, GraphqlApiExtension
from support import return_id_input
from support.common_object.tree_object import TreeObject

from Schema import Query, Mutation, DepartmentTreeFilter, CreateDepartmentInput, DepartmentNameSameAsSiblingsFilter, \
    UpdateDepartmentInput, DeleteDepartmentsInput


class Company(GraphqlApi):
    api = Query.company

    def query(self, company_id):
        return self.run(id=company_id)


class UpdateCompany(GraphqlApiExtension.GraphqlOperationAPi):
    api = Mutation.update_company


# 组织架构树
class DepartmentTreeObject(TreeObject):
    parent_field = "parent_id"
    child_field = "children"


class DepartmentTree(GraphqlApi):
    api = Query.department_tree

    def query(self, company_id):
        self.run(filter=DepartmentTreeFilter(company=return_id_input(company_id)))
        return DepartmentTreeObject(**json.loads(self.result.obj))

    def search(self, company_id, path):
        tree = self.query(company_id)
        names = path.split(".")
        node = tree
        for name in names:
            node = node.select_deep("name", name)
        return node


class CreateDepartment(GraphqlApi):
    api = Mutation.create_department

    def create(self, name, parent_node):
        return self.run(input=CreateDepartmentInput(name=name, parent=return_id_input(parent_node.id)))


class DepartmentNameSameAsSiblings(GraphqlApi):
    api = Query.department_name_same_as_siblings

    def _query(self, **kwargs):
        return self.run(input=DepartmentNameSameAsSiblingsFilter(**kwargs))

    def query_create(self, parent_node, name):
        """新建时候用"""
        return self._query(name=name, parent=return_id_input(parent_node.id))

    def query_update(self, node, parent_node, name):
        return self._query(id=node.id, name=name, parent=return_id_input(parent_node.id))


class UpdateDepartment(GraphqlApi):
    api = Mutation.update_department

    def update_name(self, node, name):
        return self.run(input=UpdateDepartmentInput(id=node.id, name=name))

    def update_position(self, node, parent_node):
        return self.run(input=UpdateDepartmentInput(id=node.id, parent=return_id_input(parent_node.id)))


class DeleteDepartment(GraphqlApi):
    api = Mutation.delete_department

    def delete(self, node):
        return self.run(input=DeleteDepartmentsInput(ids=[node.id]))


class DepartmentOperator:

    def __init__(self, user, company_id):
        self.user = user
        self.company_id = company_id
        self.query = DepartmentTree(self.user)
        self.create = CreateDepartment(self.user)
        self.delete = DeleteDepartment(self.user)
        self.update = UpdateDepartment(self.user)
        self.assert_department = DepartmentNameSameAsSiblings(self.user)

    @property
    def root(self):
        return self.query.query(self.company_id)

    def search_node(self, path):
        return self.query.search(self.company_id, path)


if __name__ == '__main__':
    from support import admin

    print(DepartmentTree(admin).search(38, "新组织.新组织"))
