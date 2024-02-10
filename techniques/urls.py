from django.urls import path
from . import views

urlpatterns = [
    path('add', views.add, name='add'),
    path('private', views.private, name='private'),
    path('public', views.public, name='public'),
    path('remove/<int:technique_id>/', views.remove, name='remove'),
]