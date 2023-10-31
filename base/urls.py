from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginPage, name='login'),
    path('logout/',views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('',views.home, name='home'),
    path('room_page/<str:pk>/',views.room,name='room'),
    # path('room_page',views.room_main),
    path('create-room/',views.CreateRoom, name='create-room'),
    path('update-room/<str:pk>',views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>',views.deleteRoom, name='delete-room'),
    # added by me
    path('create-message/',views.CreateMessage, name='create-message'),
]