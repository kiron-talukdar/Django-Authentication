from typing import Any
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.views import(
    PasswordResetView,
    PasswordResetConfirmView,
)
from .forms import (
    ChangePasswordForm,
    LoginForm,
    SendEmailForm, 
    UserRegistrationForm,
    ResetPasswordConfirmForm
    )
from .mixins import LogoutRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
# Create your views here.


@method_decorator(never_cache, name='dispatch')
class Home(LoginRequiredMixin, generic.TemplateView ):
    login_url='login/'
    template_name='account/home.html'
   



@method_decorator(never_cache, name='dispatch')
class Login(  LogoutRequiredMixin,generic.View ):
    
    def get(self, *args, **kwargs):
        form=LoginForm()       #import from forms.py
        context={'form':form}
        return render(self.request, 'account/login.html', context)

    def post(self, *args, **kwargs):
        form = LoginForm(self.request.POST)

        if form.is_valid():
            user=authenticate( self.request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'),
            )
            if user:
                login(self.request, user)   #here login method is imported
                return redirect('home')
            else:
                messages.warning(self.request, "wrong credentials")
                return redirect('login')

        return render(self.request, 'account/login.html', {'form':form})
    

class Logout(generic.View):
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect ('login')
    
@method_decorator(never_cache, name='dispatch')
class Register(LogoutRequiredMixin,generic.CreateView):
    template_name='account/registration.html'
    form_class=UserRegistrationForm     #create a form class from forms.py
    success_url=reverse_lazy('login')
    #override method
    def form_valid(self, form):
        messages.success(self.request, "Registration Successful !")
        return super().form_valid(form)
    
#Change password
@method_decorator(never_cache, name='dispatch')
class ChangePassword(LoginRequiredMixin,generic.FormView):
    template_name='account/changepassword.html'

    form_class=ChangePasswordForm
    login_url=reverse_lazy('login')
    success_url=reverse_lazy('login')
        
    def get_form_kwargs(self):
        context= super().get_form_kwargs()
        context['user']=self.request.user
        return context
    
    #override method
    def form_valid(self, form):
        user=self.request.user
        user.set_password(form.cleaned_data.get('new_password1'))
        user.save()
        messages.success(self.request, "Password Changed Successfully !")
        return super().form_valid(form)
    

class SendEmailToResetPassword(PasswordResetView):
    template_name='account/password_reset.html'
    form_class=SendEmailForm

class ResetPasswordConfirm(PasswordResetConfirmView):
    template_name='account/password_reset_confirm.html'
    form_class=ResetPasswordConfirmForm
    success_url=reverse_lazy('login')

    def form_valid(self, form: Any) :
        messages.success(self.request, "password reset successfully")
        return super().form_valid(form)