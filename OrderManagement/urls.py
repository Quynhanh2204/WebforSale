# urls.py
from django.urls import path, include
from OrderManagement import api_view
from .api_view import OrderListViewSet, OrderViewSet
from OrderManagement import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'orders-detail', api_view.OrderViewSet, basename='orders-detail')
router.register(r'orders-view', api_view.OrderListViewSet, basename='orders-view')

urlpatterns = [

    path('api/', include((router.urls, 'api'))),

    path('orders/', views.order_list_view, name='order_list_view'),
    path('orders/<str:order_id>', views.order_detail, name='order_detail'),
    path('orders/<str:order_id>/confirm', views.confirm_order, name='confirm_order'),

]
