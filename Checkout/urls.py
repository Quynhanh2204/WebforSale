from django.urls import path
from . import views

urlpatterns = [
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('', views.checkout, name='checkout'),
    path('vnpay_qr/<str:order_id>/', views.vnpay_qr, name='vnpay_qr'),
    path('order_confirmation/<str:order_id>/', views.order_confirmation_view, name='order_confirmation'),
    path('check-discount/', views.check_discount, name='check_discount'),
]