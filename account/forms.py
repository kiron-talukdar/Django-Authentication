import threading
from typing import Any
from django import forms
from django.contrib.auth import get_user_model
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from django.contrib.auth.forms import PasswordResetForm   
from account.models import User

#User Login form
class LoginForm(forms.Form):
    
    username=forms.CharField(max_length=50)
    password=forms.CharField( max_length=50, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(). __init__(*args, **kwargs)

        #to get the design in template page
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control'})

# User Registration form
class UserRegistrationForm(forms.ModelForm):

    password=forms.CharField( max_length=50, widget=forms.PasswordInput)
    #create init method
    def __init__(self, *args, **kwargs):
        super(). __init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control'})

    class Meta:
        model=User
        fields=('username','email','password')

    #..............validation if username and password exists.................
    def clean_username(self,):
        username=self.cleaned_data.get('username')
        model=self.Meta.model

        if model.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("A user with the Username already exists")
        return username
    #validation if username exists
    def clean_email(self,):
        email=self.cleaned_data.get('email')
        model=self.Meta.model

        if model.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with the email already exists")
        return email

    #.............. end validation if username and password exists................

    def clean_password(self, *args, **kwargs):
        password=self.cleaned_data.get('password')
        password2=self.data.get('password2')

        if password != password2:
            raise forms.ValidationError("Password Mismatch")
        return password
    
    def save(self, commit= True, *args, **kwargs):
        user=self.instance
        user.set_password(self.cleaned_data.get('password'))

        if commit:
            user.save()
        return user



# ChangePasswordForm

class ChangePasswordForm(forms.Form):
    current_password=forms.CharField( max_length=50, widget=forms.PasswordInput)

    new_password1=forms.CharField( max_length=50, widget=forms.PasswordInput)
    new_password2=forms.CharField( max_length=50, widget=forms.PasswordInput)

    def __init__( self, user, *args, **kwargs):
        self.user=user
        super(). __init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control'})

    def clean_current_password(self, *args, **kwargs):
        current_password=self.cleaned_data.get('current_password')

        if not self.user.check_password(current_password):      
            raise forms.ValidationError("Incorrect password")
        return current_password

    #..............Change password  .................
    def clean_new_password1(self, *args, **kwargs):
        new_password1=self.cleaned_data.get('new_password1')
        new_password2=self.data.get('new_password2')

        if new_password1 != new_password2:
            raise forms.ValidationError("Password mismatch")
        return new_password1
###########################################################    

class SendEmailForm(PasswordResetForm, threading.Thread):
    def __init__( self,  *args, **kwargs):
        super(). __init__(*args, **kwargs)

        # 1 threading to send mail quickly
        threading.Thread.__init__(self)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control'})

    ### Check email is register or not
    def clean_email(self):
        if not User.objects.filter(email__iexact=self.cleaned_data.get('email')).exists():
            raise forms.ValidationError("The email is not register")
        return self.cleaned_data.get('email')



    # 2 threading run method
    def run(self) -> None:
        return super().send_mail(
            self.subject_template_name, 
            self.email_template_name, 
            self.context, 
            self.from_email, 
            self.to_email, 
            self.html_email_template_name,
            )

    #override send_mail method
    def send_mail(self, subject_template_name: str, email_template_name: str, context: dict[str, Any], from_email: str | None, to_email: str, html_email_template_name: str | None = ...) -> None:
       
            self.subject_template_name=subject_template_name
            self.email_template_name=email_template_name
            self.context=context 
            self.from_email=from_email
            self.to_email=to_email
            self.html_email_template_name=html_email_template_name
            self.start()
########################################################### 

class ResetPasswordConfirmForm(forms.Form):

    new_password1=forms.CharField( max_length=50, widget=forms.PasswordInput)
    new_password2=forms.CharField( max_length=50, widget=forms.PasswordInput)

    def __init__( self, user, *args, **kwargs):
        self.user=user
        super(). __init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control'})

    #..............Change password  .................
    def clean_new_password1(self, *args, **kwargs):
        new_password1=self.cleaned_data.get('new_password1')
        new_password2=self.data.get('new_password2')

        if new_password1 != new_password2:
            raise forms.ValidationError("Password mismatch")
        return new_password1
    
    def save(self, commit=True, *args, **kwargs):
        self.user.set_password(self.cleaned_data.get('new_password1'))

        if commit:
            self.user.save()
        return self.user