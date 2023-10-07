from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("", views.dashboard, name="dashboard"),
    path("forgotPassword/", views.forgotPassword, name="forgotPassword"),
    path("activate/<str:uidb64>/<str:token>/", views.activate, name="activate"),
    path("resetpassword_validate/<str:uidb64>/<str:token>/", views.resetpassword_validate, name="resetpassword_validate"),
    path("resetPassword/", views.resetPassword, name="resetPassword")
]
