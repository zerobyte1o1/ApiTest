from apitestbasic import GraphqlApi

from Schema import Mutation, LoginInput


class Login(GraphqlApi):
    api = Mutation.login

    def login(self, account, password):
        return self.run(input=LoginInput(account=account, password=password))
