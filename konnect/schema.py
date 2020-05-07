import graphene
from user import schema as user_schema


class Query(
    graphene.ObjectType,
    user_schema.Query
):
    """ Root level Query ObjectType """
    pass


class Mutation(
    graphene.ObjectType,
    user_schema.Mutation
):
    """ Root level Mutation ObjectType """
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
