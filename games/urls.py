from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("home/", views.home, name="home"),
    path("game/<int:id>/", views.game_detail, name = "game_detail"),
    path("add-to-cart/<int:id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart, name="cart"),
    path("cart/increase/<int:id>/", views.increase_cart, name="increase_cart"),
    path("cart/decrease/<int:id>/", views.decrease_cart, name="decrease_cart"),
    path("cart/remove/<int:id>/", views.remove_from_cart, name="remove_from_cart"),
    path("genre/<int:id>/", views.genre_games, name="genre_games"),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]