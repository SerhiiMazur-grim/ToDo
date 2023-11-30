from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm, CustomUserLoginForm


class CreateUserView(View):
    template_name = 'users/registration.html'

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            password = form.cleaned_data['password']
            re_password = form.cleaned_data['re_password']
            
            if password != re_password:
                form.add_error('re_password', _('Passwords do not match'))
                return render(request, self.template_name, {'form': form})
            
            # Збереження користувача
            user = form.save(commit=False)
            user.set_password(password)
            user.save()
            
            return HttpResponseRedirect(reverse_lazy('login'))
            
        return render(request, self.template_name, {'form': form})


class UserLoginView(LoginView):
    form_class = CustomUserLoginForm
    next_page = '/tasks/?done=False'
    template_name = 'users/login.html'


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')
