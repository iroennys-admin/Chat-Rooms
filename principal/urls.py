from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('room/<int:id>/', views.room, name="room"),
    path('create-room/', views.createRoom, name="create-room"),
    path('edit-room/<int:id>/', views.updateRoom, name="edit-room"),
    path('delete-room/<int:id>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<int:id>/', views.deleteMessage, name="delete-message"),
    path('profile/<str:id>/', views.profile, name="user-profile"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
]
