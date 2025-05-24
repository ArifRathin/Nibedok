from django.urls import path
from .views import signUp, logIn, logOut, profile
from .views import send_verification_code, show_verify_account_page, verify_account, send_password_change_code, show_change_password_page, change_password, update_profile, update_password
urlpatterns = [
    path('sign-up', signUp, name='sign-up'),
    path('log-in', logIn, name='log-in'),
    path('log-out', logOut, name='log-out'),
    path('profile/<str:group_name>', profile, name='profile'),
    path('send-verification-code', send_verification_code, name='send-verification-code'),
    path('show-verify-account-page/<str:email>', show_verify_account_page, name='show-verify-account-page'),
    path('verify-account', verify_account, name='verify-account'),
    path('send-password-change-code', send_password_change_code, name='send-password-change-code'),
    path('show-change-password-page/<str:email>', show_change_password_page, name='show-change-password-page'),
    path('change-password', change_password, name='change-password'),
    path('update-profile', update_profile, name='update-profile'),
    path('update-password', update_password, name='update-password')
]