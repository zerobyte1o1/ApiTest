import random
from apitestbasic import fake
from faker.providers import BaseProvider
from faker import Faker


def create_str(name):
    return "_".join(["api_test", name, "".join(random.sample('zyxwvutsrqponmlkjihgfedcba', 5))])


class ExtendProvider(BaseProvider):
    fake = Faker(['zh_CN'])

    def phone(self):
        return self.fake.phone_number()

    def address(self):
        return self.fake.building_number()


fake.add_provider(ExtendProvider)
