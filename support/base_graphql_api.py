from apitestbasic import GraphqlApi, Decorator


class QueryAllApi(GraphqlApi):

    @Decorator.set_full_query()
    def run(self, *args, **kwargs):
        self.api_op(*args, **kwargs)
