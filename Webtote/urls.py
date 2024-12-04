from django.contrib import admin
from django.urls import path
from .import views

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/',views.register, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('', views.base, name = "base"),
    # path('profile/edit/', views.edit_profile, name='edit_profile'),
    # path('forgot-password/', views.forgot_password_view, name='forgot_password'),

    path('chinh-sach-doi-tra/', views.csdoi_tra),
    path('chinh-sach-thanh-toan/', views.csthanh_toan),
    path('chinh-sach-giao-hang/', views.csgiao_hang),
    path('huong-dan-mua-hang/', views.hd_mua),

]