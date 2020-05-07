from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    """ Custom user manager for custom user model """
    def create_user(self, username, email, password=None, **extra_fields):
        """ Creates and saves a new user """
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password):
        """ Creates and saves a superuser """
        user = self.create_user(username=username, email=self.normalize_email(email), password=password)
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom User model for authentication """
    username = models.CharField("Username", max_length=255, unique=True)
    email = models.EmailField("Email", max_length=255, unique=True)
    mobile = models.CharField("Mobile", max_length=17, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField("date joined", auto_now_add=True)
    updated = models.DateTimeField("Updated", auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Profile(models.Model):
    """ Profile model for user, contains user profile details """
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    )
    user = models.OneToOneField("User", on_delete=models.CASCADE, primary_key=True, related_name="profile")
    first_name = models.CharField("First name", max_length=255)
    last_name = models.CharField("Last name", max_length=255)
    gender = models.CharField("Gender", max_length=10, choices=GENDER)
    dob = models.DateField("DOB", blank=True, null=True)
    friends = models.ManyToManyField(User, related_name="friends", blank=True)
    updated = models.DateTimeField("Updated", auto_now=True)

    def __str__(self):
        return self.user.username
