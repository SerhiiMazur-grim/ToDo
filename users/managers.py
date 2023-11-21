from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUserModel.

    Methods:
        create_user: Creates a basic user with required fields and default permissions.
        create_superuser: Creates a superuser with additional staff and superuser permissions.
        update_user: Updates the user's attributes and password.

    Notes:
        This manager provides methods for creating, updating, and managing users.
        It handles field validations and necessary checks while creating or updating users.
    """
           
    def create_user(self, first_name, last_name, email, password, **extra_fields):
        """
        Create a basic user.

        Args:
            first_name (str): The user's first name.
            last_name (str): The user's last name.
            email (str): The user's email address.
            password (str): The user's password.
            **extra_fields: Additional fields for user creation.

        Returns:
            User: The created user object.

        Raises:
            ValueError: If required fields are missing.
        """
        
        if email:
            email = self.normalize_email(email)
            validate_email(email)
        else:
            raise ValueError(_('Base User: and email address is reauired'))
        
        if not first_name:
            raise ValueError(_('Users must submit a first name'))
        
        if not last_name:
            raise ValueError(_('Users must submit a last name'))
                
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields
        )
        
        user.set_password(password)
        
        user.save()
        return user
    
    
    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        """
        Create a superuser.

        Args:
            first_name (str): The superuser's first name.
            last_name (str): The superuser's last name.
            email (str): The superuser's email address.
            password (str): The superuser's password.
            **extra_fields: Additional fields for superuser creation.

        Returns:
            User: The created superuser object.

        Raises:
            ValueError: If required fields are missing or superuser permissions are incorrect.
        """
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superusers must have is_superuser=True'))
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superusers must have is_staff=True'))
        
        if not password:
            raise ValueError(_('Superusers must have a password'))

        if email:
            email = self.normalize_email(email)
            validate_email(email)
        else:
            raise ValueError(_('Admin User: and email address is required'))
        
        user = self.create_user(first_name, last_name, email, password, **extra_fields)
        
        return user
    
    
    def update_user(self, user, password=None, **extra_fields):
        """
        Update an existing user.

        Args:
            user (User): The user object to update.
            password (str): The new password for the user (optional).
            **extra_fields: Additional fields to update.

        Returns:
            User: The updated user object.
        """
        
        if password is not None:
            user.set_password(password)

        for field, value in extra_fields.items():
            setattr(user, field, value)
        
        user.save()
        
        return user
