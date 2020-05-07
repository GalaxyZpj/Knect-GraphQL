from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType, DjangoConnectionField

from .models import Profile


# QUERY CODE

class UserType(DjangoObjectType):
    """ DjangoObjectType defination for User model """
    class Meta:
        model = get_user_model()


class ProfileType(DjangoObjectType):
    """ DjangoObjectType defination for Profile model """
    class Meta:
        model = Profile


# MUTATION CODE

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


class CreateUser(graphene.Mutation):
    """ Mutation to create a user and its profile """
    class Arguments:
        user_data = UserInput(required=True)
    
    user = graphene.Field(UserType)

    def mutate(self, info, user_data=None):
        user_model_data = {
            'username': user_data.user.username,
            'email': user_data.user.email,
            'mobile': user_data.user.mobile,
            'password': user_data.user.password,
        }
        profile_model_data = {
            'first_name': user_data.profile.first_name,
            'last_name': user_data.profile.last_name,
            'gender': user_data.profile.gender,
            'dob': user_data.profile.dob,
        }
        user = get_user_model().objects.create_user(**user_model_data)
        Profile.objects.create(user=user, **profile_model_data)
        return CreateUser(user=user)


# APP LEVEL QUERY AND MUTATIONS

class Query(object):
    """ App level Query object for 'user' app """
    user = graphene.Field(UserType, user_id=graphene.String())
    user_list = graphene.List(UserType)

    def resolve_user(self, info, user_id):
        return get_user_model().objects.get(pk=user_id)
    
    def resolve_user_list(self, info):
        return get_user_model().objects.all()


class Mutation(object):
    """ App level Mutation object for 'user' app """
    create_user = CreateUser.Field()
