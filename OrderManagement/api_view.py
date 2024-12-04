from rest_framework import generics
from rest_framework import viewsets
from Webtote.models import Order, OrderDetail
from .serializers import OrderListSerializer, OrderSerializer


class OrderListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'Order_ID'

