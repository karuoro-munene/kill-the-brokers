from django.urls import path

from kill import views

urlpatterns = [
    path("", views.APIRoot.as_view()),
    path("client/register", views.UserCreateView.as_view(), name="user-register"),
    path("client/login", views.UserLoginView.as_view(), name="user-login"),
    path('client/logout', views.logout_view, name="user-logout"),
    path('client/profile/<int:id>', views.profile, name="user-profile"),
    path('client/products/all', views.all_products, name="user-products"),
    path('client/products/<int:id>', views.product, name="user-product-details"),
    path('client/products/<int:id>/images', views.product_images, name="user-product-images"),
]
