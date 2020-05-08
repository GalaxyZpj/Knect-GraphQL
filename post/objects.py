from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload

from .models import *


class PostType(DjangoObjectType):
    """
    ObjectType representation for Post model.\n
    User can add a post to his wall, tagging friends, uploading images/videos/gifs,
    also has like, comment and even replying to the comments functionality.
    """
    class Meta:
        model = Post

    liked = graphene.Boolean()

    def resolve_liked(self, info):
        return True if info.context.user in self.users_liked.all() else False


class PostFeelingType(DjangoObjectType):
    """
    ObjectType representation for PostFeeling model.\n
    User can add an expression or feeling to their posts.
    """
    class Meta:
        model = PostFeeling


class PostActivityType(DjangoObjectType):
    """
    ObjectType representation for PostActivity model.\n
    User can mension their activity in the posts.
    """
    class Meta:
        model = PostActivity


class PostSubActivityType(DjangoObjectType):
    """
    ObjectType representation for PostSubActivity model.\n
    User can elaborate their activity by choosing a sub activity while creating a posts.
    """
    class Meta:
        model = PostSubActivity


class PostImageType(DjangoObjectType):
    """
    ObjectType representation for PostImage model.\n
    User can add multiple images in their posts.
    """
    class Meta:
        model = PostImage


class PostVideoType(DjangoObjectType):
    """
    ObjectType representation for PostVideo model.\n
    User can add multiple videos in their posts.
    """
    class Meta:
        model = PostVideo


class PostGIFType(DjangoObjectType):
    """
    ObjectType representation for PostGIF model.\n
    User can add multiple gifs in their posts.
    """
    class Meta:
        model = PostGIF


class CommentType(DjangoObjectType):
    """
    ObjectType representation for Comment model.\n
    User can comment on the posts.
    """
    class Meta:
        model = Comment


class SubCommentType(DjangoObjectType):
    """
    ObjectType representation for SubComment model.\n
    Users can reply to the comment on the posts.
    """
    class Meta:
        model = SubComment


class PostInput(graphene.InputObjectType):
    """ InputObjectType defination for adding a post """
    share_with = graphene.String(required=True)
    content = graphene.String(required=True)
    friends_tagged = graphene.List(graphene.NonNull(graphene.String))
    feeling_id = graphene.String(required=False)
    sub_activity_id = graphene.String(required=False)
    location = graphene.String(required=False)
    images = graphene.List(graphene.NonNull(Upload))
    videos = graphene.List(graphene.NonNull(Upload))
    gifs = graphene.List(graphene.NonNull(Upload))
