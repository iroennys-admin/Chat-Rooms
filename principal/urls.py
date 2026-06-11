from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name="home"),
    path('room/<int:id>', views.room, name="room"),
    path('create-room/', views.createRoom, name="create-room"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name = 'registro'),
    path('delete-message/<str:id>/', views.deleteMessage, name='delete-message'),
    path('profile/<str:id>/', views.profile, name = 'user-profile'),
    path('createRoom/', views.createRoom, name = 'create-room'),
    path('delete-room/<str:id>/', views.deleteRoom, name = 'delete-room'),
    
]





