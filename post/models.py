from django.db import models
from django.contrib.auth import get_user_model


class PostFeeling(models.Model):
    name = models.CharField("Feeling", max_length=64, blank=False)
    emoticon = models.FileField("Feeling Emoticon", upload_to="post/emoticons", blank=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PostActivity(models.Model):
    name = models.CharField("Activity Name", max_length=64, blank=False)
    emoticon = models.FileField("Activity Emoticon", upload_to="post/activities/emoticons", blank=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PostSubActivity(models.Model):
    activity = models.ForeignKey(PostActivity, related_name="sub_activities", on_delete=models.CASCADE, blank=False)
    name = models.CharField("Activity Name", max_length=64, blank=False)
    emoticon = models.FileField("Activity Emoticon", upload_to="post/sub_activities/emoticons", blank=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    SHARE_WITH = [
        ('public', 'Public'),
        ('friends', 'Friends'),
        ('only_me', 'Only Me'),
    ]
    user = models.ForeignKey(get_user_model(), related_name='posts', on_delete=models.CASCADE, blank=False)
    share_with = models.CharField('Share With', max_length=32, choices=SHARE_WITH, blank=False)
    content = models.TextField('Content', max_length=8192, blank=False)
    likes = models.IntegerField("Likes", default=0, blank=False)
    users_liked = models.ManyToManyField(get_user_model(), related_name="users_liked", blank=True)
    friends_tagged = models.ManyToManyField(get_user_model(), related_name="friends_tagged", blank=True)
    feeling = models.ForeignKey(PostFeeling, on_delete=models.CASCADE, blank=True, null=True)
    activity = models.ForeignKey(PostActivity, on_delete=models.CASCADE, blank=True, null=True)
    location = models.URLField("Location", blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def like(self):
        self.likes = self.likes + 1
        self.save()

    def __str__(self):
        return self.user.username


class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name="images", on_delete=models.CASCADE, blank=False)
    image = models.FileField("Post Image", upload_to="post/images", blank=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post.user.username


class PostVideo(models.Model):
    post = models.ForeignKey(Post, related_name="videos", on_delete=models.CASCADE, blank=False)
    video = models.FileField("Post Video", upload_to="post/videos", blank=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post.user.username


class PostGIF(models.Model):
    post = models.ForeignKey(Post, related_name="gifs", on_delete=models.CASCADE, blank=False)
    gif = models.FileField("Post GIF", upload_to="post/gifs", blank=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post.user.username


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=False)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE, blank=False)
    content = models.TextField("Comment Content", max_length=8192, blank=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post


class SubComment(models.Model):
    comment = models.ForeignKey(Comment, related_name="sub_comments", on_delete=models.CASCADE, blank=False)
    content = models.TextField("SubComment Content", max_length=8192, blank=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment
