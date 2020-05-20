import graphene
from graphql_jwt.decorators import login_required
from user.objects import *


class Query(object):
    friend_list = graphene.List(UserType)

    @login_required
    def resolve_friend_list(self, info, **kwargs):
        return info.context.user.profile.friends.all()

    