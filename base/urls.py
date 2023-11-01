from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("", views.home, name="home"),
    path("room_page/<str:pk>/", views.room, name="room"),
    path("profile/<str:pk>/", views.userProfile, name="user-profile"),
    path("create-room/", views.CreateRoom, name="create-room"),
    path("update-room/<str:pk>", views.updateRoom, name="update-room"),
    path("delete-room/<str:pk>", views.deleteRoom, name="delete-room"),
    path("delete-comment/<str:pk>", views.deleteComment, name="delete-comment"),
    # added by me
    path(
        "delete-room-comment/<str:room_pk>/<str:message_pk>/",
        views.deleteRoomComment,
        name="delete-room-comment",
    ),
]
