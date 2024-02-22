from django.urls import path
from . import views

urlpatterns = [
    path('playlist/', views.find_playlist, name='find_playlist'),
    path('add/', views.add_to_playlist, name='add_to_playlist'),
    path('extract/<int:technique_id>/<str:playlist>/', views.extract_from_playlist, name='extract'),
    path('edit/<int:playlist_id>/', views.edit_playlist, name='edit_playlist'),
    path('all', views.all_playlists, name='all_playlists'),
    path('delete/<int:playlist_id>/', views.delete_whole_playlist, name='delete_playlist'),
]