from django.urls import path
from backend import views

urlpatterns = [
    path('api', views.apiOverview, name='apiOverview'),
    path('', views.index, name='index'),
    path('dashboard/<str:username>', views.dashboard, name='dashboard'),
    path('add_song_info', views.add_song_info, name='add_song_info'),
    path('upload_song', views.Upload_Song.as_view(), name='add_songs'),
    path('display_songs', views.display_songs, name='display_songs'),
    path('generate_playlist', views.generate_playlist, name='generate_playlist'),
    # path('test', views.test, name='test'),
    path('login_check', views.login_check, name='login_check'),
    path('signup_check', views.signup_check, name='signup_check'),
    path('logout', views.logout, name='logout'),
    path('upload_avatar/<str:username>', views.UserAvatarUpload.as_view(), name='upload_avatar')
    
]
