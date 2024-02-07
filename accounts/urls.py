from django.urls import path
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('user/<int:user_id>/', views.user, name='user'),
    path('edit', views.edit, name='edit'),
    path('password', views.password, name='password'),
    path('password/change/', PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password/change/done/', views.password_change_done, name='password_change_done'),
    path('logout', views.logout, name='logout'),
]