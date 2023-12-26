from django.urls import path
from django.contrib.auth.views import(
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,

)
# from account import views
from .views import(
    Home,
    Login,
    Logout,
    Register,
    ChangePassword,
    SendEmailToResetPassword,
    ResetPasswordConfirm,
)

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('registration/', Register.as_view(), name='register'),
    path('changepassword/',ChangePassword.as_view(), name='changepassword' ),
    path('password_reset/', SendEmailToResetPassword.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),name='password_reset_done' ),
    path('reset/<uidb64>/<token>', ResetPasswordConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/',PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    
]

# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']