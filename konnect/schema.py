import graphene
import graphql_jwt
from graphene_django.debug import DjangoDebug


from user import schema as user_schema
from post import schema as post_schema
from dashboard import schema as dashboard_schema
from user.objects import UserType


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class Query(
    graphene.ObjectType,
    user_schema.Query,
    post_schema.Query,
    dashboard_schema.Query
):
    """ Queries available in the schema """
    debug = graphene.Field(DjangoDebug, name='_debug')


class Mutation(
    graphene.ObjectType,
    user_schema.Mutation,
    post_schema.Mutation
):
    """ Mutations available in the schema """
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
