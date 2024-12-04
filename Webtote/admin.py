from django.contrib import admin
from .models import (Customer, Discount, Order,ProductCategory,Product,ReviewProduct, OrderDetail)
from django.utils.html import format_html
from .forms import ProductForm

class OrderAdmin(admin.ModelAdmin):
    list_display = ('Order_ID', 'Customer','Order_Status', 'Total_Price','Discount','Payment_Status','Shipment_Status')  # Thay đổi theo các trường trong model của bạn
    search_fields = ('Order_ID', 'Order_Status')
    list_filter = ('Order_ID', 'Order_Status')
admin.site.register(Order, OrderAdmin)

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('Category_Name',)
    search_fields = ('Category_Name',)
    ordering = ('Category_Name',)
admin.site.register(ProductCategory, ProductCategoryAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('Name', 'UserName', 'Email', 'Password')  # Thêm các trường bạn muốn hiển thị
    search_fields = ('Name', 'Email',)
admin.site.register(Customer, CustomerAdmin)


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('Discount_Code', 'formatted_discount_value', 'Start_Date', 'End_Date','is_active')  # Các trường cần hiển thị trong danh sách
    list_filter = ('is_active', 'Start_Date')  # Bộ lọc theo trạng thái và ngày bắt đầu
    search_fields = ('Discount_Code',)  # Tìm kiếm theo tên khuyến mãi
    def formatted_discount_value(self, obj):
        if obj.Discount_Value is not None:
            return f"{obj.Discount_Value * 100:.0f}%"  # Chuyển đổi thành phần trăm và bỏ phần thập phân nếu không cần
        return None  # Trường hợp không có giá trị
    formatted_discount_value.short_description = 'Discount Value'
    def is_active(self, obj):
        return obj.is_active  # Logic để xác định khuyến mãi đang hoạt động
    is_active.boolean = True  # Hiển thị biểu tượng True/False

admin.site.register(Discount,DiscountAdmin)


class PriceRangeFilter(admin.SimpleListFilter):
    title = 'Unit Price Range'
    parameter_name = 'unit_price_range'

    def lookups(self, request, model_admin):
        return [
            ('low', 'Dưới 50,000'),
            ('medium', '50,000 - 100,000'),
            ('high', 'Trên 100,000'),
        ]
    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(Unit_Price__lt=50000)
        elif self.value() == 'medium':
            return queryset.filter(Unit_Price__gte=50000, Unit_Price__lte=100000)
        elif self.value() == 'high':
            return queryset.filter(Unit_Price__gt=100000)
        return queryset

class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('Product_Name', 'Color', 'Unit_Price', 'Quantity', 'Date_Created', 'Date_Edited', 'show_orders', 'image_tag')
    list_filter = (PriceRangeFilter,'Date_Created', 'Color', 'Unit_Price')
    search_fields = ('Product_Name', 'Description')
    ordering = ('Date_Created',)
    list_editable = ('Unit_Price', 'Quantity')
    def image_tag(self, obj):
        primary_image = obj.productimage_set.filter(Is_Primary=True).first()
        if primary_image and primary_image.Image_Url:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 5px;" alt="{}" />',
                primary_image.Image_Url, primary_image.Alt_Text)
        return "-"
    image_tag.short_description = 'Primary Image'
    def show_orders(self, obj):
        return ", ".join([str(order) for order in obj.Order.all()])
    show_orders.short_description = 'Orders'
admin.site.register(Product, ProductAdmin)


class ReviewProductAdmin(admin.ModelAdmin):
        list_display = ('Customer','Order_Detail', 'Rating', 'Content','Date_Created')
        list_filter = ('Order_Detail', 'Rating', 'Date_Created')
        search_fields = ('Order_Detail', 'Content')

admin.site.register(ReviewProduct, ReviewProductAdmin)

admin.site.register(OrderDetail)
