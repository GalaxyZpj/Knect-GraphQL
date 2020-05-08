from .objects import *
from .mutations import *

from user.objects import UserType


class Query(object):
    post = graphene.Field(PostType, post_id=graphene.String(required=True), description='''
        Fetches a post corresponding to a postId
        '''
                          )
    my_posts = graphene.List(PostType, description='''
        Fetches all the posts corresponding to the current logged in user
        '''
                             )
    friend_posts = graphene.List(PostType, friend_id=graphene.String(required=True), description='''
        Fetches posts corresponding to a userId of a friend
        '''
                                 )
    all_friends_posts = graphene.List(PostType, description='''
        Fetches all posts from every friend
        '''
                                      )

    @login_required
    def resolve_post(self, info, post_id, **kwargs):
        return Post.objects.get(pk=post_id)

    @login_required
    def resolve_my_posts(self, info, **kwargs):
        return Post.objects.filter(user=info.context.user)

    @login_required
    def resolve_friend_posts(self, info, friend_id, **kwargs):
        return Post.objects.filter(user_id=friend_id, share_with__in=['public', 'friends'])

    @login_required
    def resolve_all_friends_posts(self, info, **kwargs):
        return Post.objects.filter(user_id__in=info.context.user.profile.friends.all())


class Mutation(object):
    create_feeling = CreateFeeling.Field()
    create_activity = CreateActivity.Field()
    create_sub_activity = CreateSubActivity.Field()
    create_post = CreatePost.Field()
    delete_post = DeletePost.Field()
    create_comment = CreateComment.Field()
    delete_comment = DeleteComment.Field()
    create_sub_comment = CreateSubComment.Field()
    delete_sub_comment = DeleteSubComment.Field()
    like_post = LikePost.Field()
    unlikePost = UnlikePost.Field()
