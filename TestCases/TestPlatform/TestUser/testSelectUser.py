from Apis.PlatformBaseApi.UserApi import *
from Apis.PlatformBaseApi.CompanyApi import CompanyTypeList, TypeCompanies
import allure
import random


class TestSelectUser:
    @allure.title('展示用户列表')
    def test1(self):
        assert Users(admin).users("company={'id':'36'}").result



if __name__ == '__main__':
    from support import run

    run(__file__)
