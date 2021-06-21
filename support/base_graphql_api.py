from apitestbasic import GraphqlApi, Decorator


class QueryAllApi(GraphqlApi):

    @Decorator.set_fields()
    def run(self, *args, **kwargs):
        self.api_op(*args, **kwargs)
