from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='/profile/'), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('company/', views.CompanyView.as_view(), name='company'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path(
        'password-reset/confirm/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path('password-reset/complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
