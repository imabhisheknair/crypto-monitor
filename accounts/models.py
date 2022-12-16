from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
  

class AccountManager(BaseUserManager):
    def create_user(self, email, username, is_staff=False, password=None):
        if not email:
            raise ValueError('You must have an email')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            is_active = 1,
            is_staff = is_staff,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    

    def create_superuser(self, email, username, password=None):
        if not email:
            raise ValueError('You must have an email')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            is_active = 1,
            is_superuser = 1,
            is_admin = 1,
            is_staff = 1
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    chatid = models.CharField(max_length=100, default="")

    USERNAME_FIELD='username'

    REQUIRED_FIELD = ['email', 'username', 'password']

    objects = AccountManager()

