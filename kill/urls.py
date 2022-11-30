from django.urls import path

from kill import views

urlpatterns = [
    path("", views.APIRoot.as_view()),
    path("client/register", views.UserCreateView.as_view(), name="user-register"),
    path("client/login", views.UserLoginView.as_view(), name="user-login"),
    path('client/logout', views.logout_view, name="user-logout"),
    path('client/profile/<int:id>', views.profile, name="user-profile"),

]