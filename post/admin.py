from django.contrib import admin

from .models import *

admin.site.register(PostFeeling)
admin.site.register(PostActivity)
admin.site.register(PostSubActivity)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(SubComment)
