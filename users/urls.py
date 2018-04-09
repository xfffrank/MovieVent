from django.urls import path
from .import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('account/', views.account, name='account'),
    path('user/<int:user_id>', views.user_center, name='homepage'),
    # path('password_reset', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset', views.password_reset_x, name='password_reset_X'),
    path('account/suicide', views.delete_account, name='delete_account'),
]