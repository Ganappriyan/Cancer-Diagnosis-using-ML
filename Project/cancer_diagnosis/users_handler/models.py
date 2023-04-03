# diagnosis/models.py

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, email=None, phone=None, public_key=None, role=None):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
            email=email,
            phone=phone,
            public_key=public_key,
            role=role,
        )

        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email=None, phone=None, public_key=None, role=None):
        user = self.create_user(
            username=username,
            password=password,
            email=email,
            phone=phone,
            public_key=public_key,
            role=role,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    public_key = models.CharField(max_length=1000, blank=True, null=True)
    role = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'username'
    objects = UserManager()

    def __str__(self):
        return self.username

    def check_password(self, raw_password):
        """
        Return a boolean indicating whether the raw_password matches the stored password hash.
        """
        return check_password(raw_password, self.password)
