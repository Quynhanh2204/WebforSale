from django.urls import path
from . import views
urlpatterns = [
    path('', views.product_list,name='product_list'),
    path('category/<int:category_id>/', views.product_list, name='category_product_list'),
    path('search/',views.search_products,name='search_products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # path('checkout', views.checkout, name='checkout'),
    path('detail/<int:product_id>/', views.product_detail, name='product_detail'),

]