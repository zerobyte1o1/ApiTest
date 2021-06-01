from Apis.PlatformBaseApi.CreateCompany import *
import allure
import random
from support import assert_true


class TestCreateCompany:

    @allure.title("查询企业类型和列表")
    def test1(self, admin):
        assert TypeCompanies(admin).run().result

    @allure.title("查询省份")
    def test2(self, admin):
        assert Provinces(admin).run().result

    @allure.title("查询市")
    def test3(self, admin):
        province_id = random.choice(Provinces(admin).run().result.id)
        assert Cities(admin).cities(province_id).result

    @allure.title("查询区")
    def test4(self, admin):
        province_id = random.choice(Provinces(admin).run().result.id)
        city_id = random.choice(Cities(admin).cities(province_id).result.id)
        assert Counties(admin).counties(city_id).result

    @allure.title("查询企业类型列表")
    def test5(self, admin):
        assert CompanyTypeList(admin).run().result

    @allure.title("创建企业")
    def test6(self, admin):
        c = CreateCompany(admin)
        c.create_company(name="接口测试1", phone="15774510000",
                         province="浙江省", city="杭州市", county="萧山区",
                         address="测试")
        assert_true(c.result)


if __name__ == '__main__':
    from support import run

    run(__file__)
