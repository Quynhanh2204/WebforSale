from rest_framework import serializers
from Webtote.models import (Order, Customer, PaymentStatus, ShipmentStatus, OrderDetail, Product, ProductImage,
                            DeliveryInformation)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'Product_Name',
            'Unit_Price',
            'Color',
        ]

class OrderDetailSerializer(serializers.ModelSerializer):
    Product = ProductSerializer(read_only=True)
    ProductImage = serializers.SerializerMethodField("get_ProductImage")
    class Meta:
        model = OrderDetail
        fields = [
            'Product',
            'ProductImage',
            'Quantity',
            'Subtotal',
        ]

    def get_ProductImage(self, obj):
        # Lấy ảnh chính (primary image) của sản phẩm
        primary_image = obj.Product.productimage_set.filter(Is_Primary=True).first()
        return primary_image.Image_Url if primary_image else None

class DeliveryInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryInformation
        fields = [
            'Name',
            'Phone_Number',
            'Address',
        ]

class OrderSerializer(serializers.ModelSerializer):
    orderdetail = OrderDetailSerializer(many=True, read_only=True)
    Delivery_Infor = DeliveryInformationSerializer(read_only=True)
    payment_method = serializers.CharField(source='Payment_Method.Method_Name')
    shipment_method = serializers.CharField(source='Shipment_Method.Method_Name')


    class Meta:
        model = Order
        fields = [
            'Order_ID',
            'Order_Status',
            'Order_Date',
            'Total_Price',
            'orderdetail',
            'payment_method',  # Thêm phương thức thanh toán
            'shipment_method',  # Thêm phương thức vận chuyển
            'Delivery_Infor',
            'Reason',
            'Cancel_Date',
            'get_Reason_display',
            'Return_Date',
            'Return_Reason',
            'get_Return_Reason_display',
        ]

class OrderListSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='Customer.Name')
    customer_id = serializers.CharField(source='Customer.id')
    payment_status = serializers.CharField(source='Payment_Status')
    shipment_status = serializers.CharField(source='Shipment_Status')

    class Meta:
        model = Order
        fields = [
            'Order_ID',
            'customer_name',
            'customer_id',
            'Order_Status',
            'payment_status',
            'shipment_status',
            'Order_Date',
            'Total_Price',
        ]

