from django.conf.urls import url
from .import views

app_name = 'users'
urlpatterns = [
    url('register/', views.register, name='register'),
    url('account_management/', views.account, name='account'),
    url('user/', views.user_center, name='user'),

]