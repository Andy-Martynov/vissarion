from django.urls import path

from . import views

app_name='account'
urlpatterns = [
    path("confirm/<int:token>", views.confirm_email, name="confirm"),
    path("register", views.register, name="register"),
]