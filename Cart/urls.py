from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:cart_item_id>/', views.update_cart_item, name='update_cart_item'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('checkout/', views.checkout, name='checkout'),
]