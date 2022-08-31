from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'forms'
urlpatterns = [
    path('', views.IndexView, name='index'),
    path('accounts/login/', auth_views.LoginView.as_view()),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("accounts/profile/", views.Profile, name = 'profile'),
    path("accounts/change_password/", views.Change_Password, name = 'change_password'),
    path("make_post/", views.Make_Post, name = 'make_post'),
    path("user/<int:pk>/", views.UserView, name ="user"),
    path("post/<int:pk>/", views.PostView, name="post"),
    path("comment/<int:pk>/", views.CommentView, name="comment"),
    path("search/", views.SearchView, name="search")
]