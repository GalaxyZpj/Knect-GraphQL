from django.contrib import admin
from django.urls import path
# from graphene_django.views import GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.conf import settings

from konnect.schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True, schema=schema))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
