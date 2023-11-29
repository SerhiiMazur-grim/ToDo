from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(
        attrs={
        'class': 'form-control bg-dark text-light', 
        'type': 'password', 
        'placeholder': 'Password'
        }
    ))
    re_password = forms.CharField(label=_('Repit password'), widget=forms.PasswordInput(
        attrs={
        'class': 'form-control bg-dark text-light', 
        'type': 'password', 
        'placeholder': 'Confirm Password'
        }
    ))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 're_password']
        widgets = {
            'first_name': forms.TextInput(attrs={
            'class': 'form-control bg-dark text-light', 
            'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
            'class': 'form-control bg-dark text-light', 
            'placeholder': 'Last Name'
            }),
            'email': forms.TextInput(attrs={
            'class': 'form-control bg-dark text-light', 
            'placeholder': 'Email'
            }),
        } 


class CustomUserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder':'Enter email'
                }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder': "Password",
                }))

    # class Meta:
    #     model = User
    #     fields = ['email', 'password']
