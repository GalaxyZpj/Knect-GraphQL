from graphql_jwt.decorators import login_required

from .objects import *
from .mutations import *


class Query(object):
    """ App level Query object for 'user' app """
    user = graphene.Field(UserType, user_id=graphene.String())
    user_list = graphene.List(UserType)

    def resolve_user(self, info, user_id):
        return get_user_model().objects.get(pk=user_id)
    
    @login_required
    def resolve_user_list(self, info):
        return get_user_model().objects.all()


class Mutation(object):
    """ App level Mutation object for 'user' app """
    create_user = CreateUser.Field()
