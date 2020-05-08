from .objects import *

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
