from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model for handling user authentication and authorization.

    Attributes:
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        email (str): The user's email address (unique).
        is_staff (bool): Flag indicating if the user has staff permissions.
        is_superuser (bool): Flag indicating if the user has superuser permissions.
        is_active (bool): Flag indicating if the user account is active.
        date_joined (datetime): The date and time when the user account was created.
        
    Fields:
        USERNAME_FIELD (str): The field used as the unique identifier for authentication (email).
        REQUIRED_FIELDS (list): List of fields required when creating a user via the command line.
        objects (CustomUserManager): The manager for the CustomUserModel.

    Methods:
        get_full_name(): Returns the full name of the user combining first and last names.

    Meta:
        verbose_name (str): Singular name for the model in the admin interface.
        verbose_name_plural (str): Plural name for the model in the admin interface.

    """
    
    first_name = models.CharField(_('First Name'), max_length=100)
    last_name = models.CharField(_('Last Name'), max_length=100)
    email = models.EmailField(_('Email Address'), max_length=254, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
    
    
    def __str__(self):
        return self.email
    
    
    def __repr__(self):
        return f'<{self.__class__}: {self.email}>'
    
    
    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
