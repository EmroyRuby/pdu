from django.urls import path

from . import views

urlpatterns = [
    path('register', views.UserRegister.as_view(), name='register'),
    path('login', views.UserLogin.as_view(), name='login'),
    path('logout', views.UserLogout.as_view(), name='logout'),
    path('user', views.UserView.as_view(), name='user'),
    path('edit', views.UserEdit.as_view(), name='edit'),
    path('password_change', views.ChangePasswordView.as_view(), name='password_change')
]
