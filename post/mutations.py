from django.db.models import F
from graphql_jwt.decorators import login_required, superuser_required

from .objects import *


class CreateFeeling(graphene.Mutation):
    """ Creates Feeling for the Post Interface, can only be accessed by superuser """
    class Arguments:
        name = graphene.String(required=True)
        emoticon = Upload(required=True)

    expression = graphene.Field(PostFeelingType)

    @superuser_required
    def mutate(self, info, name, emoticon, **kwargs):
        expression = PostFeeling.objects.create(name=name, emoticon=emoticon)
        return CreateFeeling(expression=expression)


class CreateActivity(graphene.Mutation):
    """ Creates Activity for the Post Interface, can only be accessed by superuser """
    class Arguments:
        name = graphene.String(required=True)
        emoticon = Upload(required=False)
    activity = graphene.Field(PostActivityType)

    @superuser_required
    def mutate(self, info, name, emoticon=None, **kwargs):
        activity = PostActivity.objects.create(name=name, emoticon=emoticon)
        return CreateActivity(activity=activity)


class CreateSubActivity(graphene.Mutation):
    """ Creates SubActivity for the Post Interface, can only be accessed by superuser """
    class Arguments:
        activity_id = graphene.String(required=True)
        name = graphene.String(required=True)
        emoticon = Upload(required=False)

    sub_activity = graphene.Field(PostSubActivityType)

    @superuser_required
    def mutate(self, info, activity_id, name, emoticon=None, **kwargs):
        sub_activity = PostSubActivity.objects.create(
            activity_id=activity_id, name=name, emoticon=emoticon)
        return CreateSubActivity(sub_activity=sub_activity)


class CreatePost(graphene.Mutation):
    """ Creates a Post """
    class Arguments:
        post_data = PostInput(required=True)

    post = graphene.Field(PostType)
    success = graphene.Boolean()

    @login_required
    def mutate(self, info, post_data=None):
        post = Post(
            user=info.context.user,
            share_with=post_data.share_with,
            content=post_data.content,
            feeling_id=post_data.feeling_id,
            sub_activity_id=post_data.sub_activity_id,
            location=post_data.location
        )
        post.save()
        
        if post_data.friends_tagged:
            post.friends_tagged.add(*post_data.friends_tagged)

        if post_data.images:
            for image in post_data.images:
                PostImage.objects.create(post=post, image=image)

        if post_data.videos:
            for video in post_data.videos:
                PostVideo.objects.create(post=post, video=video)

        if post_data.gifs:
            for gif in post_data.gifs:
                PostImage.objects.create(post=post, gif=gif)

        return CreatePost(post=post, success=True)


class DeletePost(graphene.Mutation):
    """ Deletes a Post """
    class Arguments:
        post_id = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, post_id, **kwargs):
        try:
            post = Post.objects.select_related('user').get(pk=post_id)
            if post.user == info.context.user:
                post.delete()
                success = True
                message = "Post Deleted"
            else:
                success = False
                message = "Not authorized to delete this post"
        except Exception as e:
            success = False
            message = e
        return DeletePost(success=success, message=message)


class CreateComment(graphene.Mutation):
    """ Creates a Comment for a Post """
    class Arguments:
        post_id = graphene.String(required=True)
        content = graphene.String(required=True)

    comment = graphene.Field(CommentType)

    @login_required
    def mutate(self, info, post_id, content, **kwargs):
        comment_data = {
            'user': info.context.user,
            'post_id': post_id,
            'content': content,
        }
        comment = Comment.objects.create(**comment_data)
        return CreateComment(comment=comment)


class DeleteComment(graphene.Mutation):
    """ Deletes a Comment """
    class Arguments:
        comment_id = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, comment_id, **kwargs):
        try:
            comment = Comment.objects.select_related(
                'user', 'post__user').get(pk=comment_id)
            if comment.user == info.context.user or comment.post.user == info.context.user:
                comment.delete()
                success = True
                message = "Comment Deleted"
            else:
                success = False
                message = "Not authorized to delete this comment"
        except Exception as e:
            success = False
            message = e
        return DeleteComment(success=success, message=message)


class CreateSubComment(graphene.Mutation):
    """ Creates a reply for the Comment """
    class Arguments:
        comment_id = graphene.String(required=True)
        content = graphene.String(required=True)

    sub_comment = graphene.Field(SubCommentType)

    @login_required
    def mutate(self, info, comment_id, content, **kwargs):
        sub_comment_data = {
            'user': info.context.user,
            'comment_id': comment_id,
            'content': content,
        }
        sub_comment = SubComment.objects.create(**sub_comment_data)
        return CreateSubComment(sub_comment=sub_comment)


class DeleteSubComment(graphene.Mutation):
    """ Deletes a reply to the comment """
    class Arguments:
        sub_comment_id = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, sub_comment_id, **kwargs):
        try:
            sub_comment = SubComment.objects.select_related(
                'user', 'comment__user').get(pk=sub_comment_id)
            if sub_comment.user == info.context.user or sub_comment.comment.user == info.context.user:
                sub_comment.delete()
                success = True
                message = "SubComment Deleted"
            else:
                success = False
                message = "Not authorized to delete this subComment"
        except Exception as e:
            success = False
            message = e
        return DeleteSubComment(success=success, message=message)


class LikePost(graphene.Mutation):
    """ Adds a like to the Post """
    class Arguments:
        post_id = graphene.String(required=False)

    post = graphene.Field(PostType)

    @login_required
    def mutate(self, info, post_id, **kwargs):
        post = Post.objects.filter(pk=post_id)
        post.update(likes=F('likes')+1)
        post.first().users_liked.add(info.context.user.pk)
        return LikePost(post=post.first())


class UnlikePost(graphene.Mutation):
    """ Removes a like from the Post """
    class Arguments:
        post_id = graphene.String(required=False)

    post = graphene.Field(PostType)

    @login_required
    def mutate(self, info, post_id, **kwargs):
        post = Post.objects.filter(pk=post_id)
        post.update(likes=F('likes')-1)
        post.first().users_liked.remove(info.context.user.pk)
        return LikePost(post=post.first())
