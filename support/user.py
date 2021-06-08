from apitestbasic import BaseUser, GraphqlApi
from load_config import config
from Schema import Mutation, Query


class Me(GraphqlApi):
    api = Query.me


class User(BaseUser):
    url = config.web_config.get("url")

    def __init__(self, account, password):
        super(User, self).__init__(self.url, Mutation, {"account": account, "password": password})
        self.info = Me(self).run().result
