from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("suggest/", views.suggest, name="suggest"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("user-data/", views.user_data, name="user-data"),
    path("delete-data/<int:instance_id>/", views.delete_data, name="delete-data"),
]
