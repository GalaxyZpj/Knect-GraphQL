from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType

from .models import Profile


class UserType(DjangoObjectType):
    """ DjangoObjectType defination for User model """
    class Meta:
        model = get_user_model()


class ProfileType(DjangoObjectType):
    """ DjangoObjectType defination for Profile model """
    class Meta:
        model = Profile


class UserModelInput(graphene.InputObjectType):
    """ InputObjectType defination for User model """
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    mobile = graphene.String(required=True)
    password = graphene.String(required=True)


class ProfileModelInput(graphene.InputObjectType):
    """ InputObjectType defination for Profile model """
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    gender = graphene.String(required=True)
    dob = graphene.Date(required=True)


class UserInput(graphene.InputObjectType):
    """ InputObjectType defination for User and Profile InputTypeObjects """
    user = graphene.InputField(UserModelInput)
    profile = graphene.InputField(ProfileModelInput)
