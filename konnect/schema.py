import graphene
import graphql_jwt
from user import schema as user_schema
from post import schema as post_schema
from dashboard import schema as dashboard_schema


class Query(
    graphene.ObjectType,
    user_schema.Query,
    post_schema.Query,
    dashboard_schema.Query
):
    """ Queries available in the schema """
    pass


class Mutation(
    graphene.ObjectType,
    user_schema.Mutation,
    post_schema.Mutation
):
    """ Mutations available in the schema """
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
