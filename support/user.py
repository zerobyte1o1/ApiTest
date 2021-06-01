from apitestbasic import BaseUser
from load_config import config
from Schema import Mutation

url = config.web_config.get("url")


class User(BaseUser):

    def __init__(self, account, password):
        super(User, self).__init__(url, Mutation, {"account": account, "password": password})
