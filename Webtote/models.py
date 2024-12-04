from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


def save_user(username, password, email):
    user = User(username=username, email=email)
    user.set_password(password)  # Mã hóa mật khẩu
    user.save()


# Create your models here.
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',
                  'password1', 'password2']


# Create your models here.
class Customer(models.Model):
    Name = models.CharField(max_length=200, null=False)
    UserName = models.CharField(max_length=50, null=False, unique=True)
    Password = models.CharField(max_length=200, null=False)
    Email = models.EmailField(unique=True, null=False)

    def __str__(self):
        return self.Name


class DeliveryInformation(models.Model):  # Thong tin giao hang
    Name = models.CharField(max_length=250, null=False)  # ten nguoi nhan
    Phone_Number = models.CharField(max_length=15, null=False)
    Address = models.TextField(null=False)
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Discount(models.Model):
    Discount_Code = models.CharField(max_length=50)
    Discount_Value = models.DecimalField(max_digits=100, decimal_places=2)
    Start_Date = models.DateField()
    End_Date = models.DateField()
    is_active = models.BooleanField(default=True)
    Description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.Discount_Code


class PaymentMethod(models.Model):
    Method_Name = models.CharField(max_length=100)


class ShipmentMethod(models.Model):
    Method_Name = models.CharField(max_length=150)
    Method_Cost = models.DecimalField(max_digits=10, decimal_places=2)
    Expected_Date = models.IntegerField()


class ShipmentStatus(models.Model):
    Tracking_Number = models.CharField(primary_key=True, auto_created=True, max_length=100)

    class ShippingStatus(models.TextChoices):
        DANG_VAN_CHUYEN = 'ĐANG VẬN CHUYỂN', 'Đang vận chuyển'
        GIAO_THANH_CONG = 'GIAO THÀNH CÔNG', 'Giao thành công'
        GIAO_KHONG_THANH_CONG = 'GIAO KHÔNG THÀNH CÔNG', 'Giao không thành công'
        DA_HUY = 'ĐÃ HỦY', 'Đã hủy'
        TRA_HANG_THANH_CONG = 'TRẢ HÀNG THÀNH CÔNG', 'Trả hàng thành công'

    Shipment_Status = models.CharField(choices=ShippingStatus.choices, max_length=50)

    def __str__(self):
        return self.Shipment_Status


class PaymentStatus(models.Model):
    class Status(models.TextChoices):
        THANH_TOAN_THANH_CONG = 'THANH TOÁN THÀNH CÔNG', 'Thanh toán thành công'
        THANH_TOAN_KHONG_THANH_CONG = 'THANH TOÁN KHÔNG THÀNH CÔNG', 'Thanh toán không thành công'
        HOAN_TRA_THANH_CONG = 'HOÀN TRẢ THÀNH CÔNG', 'Hoàn trả thành công'

    Payment_Status = models.CharField(choices=Status.choices, max_length=70, blank=True)

    def __str__(self):
        return self.Payment_Status


class Order(models.Model):
    Order_ID = models.CharField(primary_key=True, auto_created=True, max_length=50)
    Order_Date = models.DateTimeField(auto_now_add=True, null=False)

    class OrderStatus(models.TextChoices):
        DON_HANG_MOI = 'ĐƠN HÀNG MỚI', 'Đơn hàng mới'
        DA_XAC_NHAN = 'ĐÃ XÁC NHẬN ĐƠN HÀNG', 'Đã xác nhận'
        DANG_VAN_CHUYEN = 'ĐANG VẬN CHUYỂN', 'Đang vận chuyển'
        GIAO_THANH_CONG = 'GIAO THÀNH CÔNG', 'Giao thành công'
        GIAO_KHONG_THANH_CONG = 'GIAO KHÔNG THÀNH CÔNG', 'Giao không thành công'
        DA_HUY = 'ĐÃ HỦY', 'Đã hủy'
        HOAN_TRA = 'HOÀN TRẢ', 'Hoàn trả'
        TRA_HANG_THANH_CONG = 'TRẢ HÀNG THÀNH CÔNG', 'Trả hàng thành công'

    CANCEL_REASONS = [
        ('update_address', 'Tôi muốn cập nhật địa chỉ/sđt giao hàng'),
        ('discount_code', 'Tôi muốn thêm/thay đổi mã giảm giá'),
        ('change_product', 'Tôi muốn thay đổi sản phẩm (màu sắc, số lượng,...)'),
        ('payment_issue', 'Thủ tục thanh toán rắc rối'),
        ('better_deal', 'Tôi tìm thấy chỗ mua khác tốt hơn (Rẻ hơn, giao nhanh hơn, uy tín hơn...)'),
        ('no_need', 'Tôi không có nhu cầu mua nữa'),
    ]

    RETURN_REASONS = [
        ('missing_items', 'Nhận thiếu hàng'),
        ('damaged', 'Đơn hàng bị hư hỏng do vận chuyển'),
        ('no_longer_needed', 'Không còn nhu cầu sử dụng'),
        ('not_as_described', 'Sản phẩm khác với mô tả'),
        ('wrong_item', 'Sản phẩm nhận được không đúng'),
    ]
    Order_Status = models.CharField(choices=OrderStatus.choices, max_length=50)
    Total_Price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    Discount = models.ForeignKey(Discount, on_delete=models.CASCADE, null=True, blank=True)
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Payment_Method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, blank=True, null=True)
    Shipment_Method = models.ForeignKey(ShipmentMethod, on_delete=models.CASCADE)
    Shipment_Status = models.ForeignKey(ShipmentStatus, on_delete=models.CASCADE, null=True, blank=True)
    Payment_Status = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE, null=True, blank=True)
    Delivery_Infor = models.ForeignKey(DeliveryInformation, on_delete=models.CASCADE)
    Reason = models.CharField(
        max_length=150,
        choices=CANCEL_REASONS,
        blank=True,
        null=True
    )
    Refund_Date = models.DateField(null=True, blank=True)
    Time_Refund_Money = models.DateTimeField(auto_now_add=True, null=True)
    Cancel_Date = models.DateField(null=True, blank=True)  # Ngày hủy
    Return_Reason = models.CharField(
        max_length=150,
        choices=RETURN_REASONS,
        blank=True,
        null=True
    )
    Return_Date = models.DateField(null=True, blank=True)  # Ngày hoàn

    def calculate_total_price(self):
        # Lấy tất cả các OrderDetail để tính tổng Subtotal
        order_details = self.orderdetail.all()  # related_name='orderdetail'
        subtotal_total = sum(detail.Subtotal for detail in order_details)

        # Lấy phí ship từ phương thức giao hàng
        shipment_cost = self.Shipment_Method.Method_Cost

        # Lấy giá trị giảm giá nếu có
        discount_value = self.Discount.Discount_Value if self.Discount else 0

        # Tính tổng tiền
        total_price = subtotal_total + shipment_cost - discount_value

        # Gán giá trị tổng tiền
        self.Total_Price = total_price

    def save(self, *args, **kwargs):
        # Tính toán tổng tiền trước khi lưu
        self.calculate_total_price()
        if not self.Order_ID:  # Chỉ tạo nếu chưa có order_id
            last_order = Order.objects.order_by('-Order_ID').first()
            if last_order:
                self.Order_ID = str(int(last_order.Order_ID) + 1)
            else:
                self.Order_ID = '100001'
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.Order_ID)


class ProductCategory(models.Model):
    Category_Name = models.CharField(max_length=100)


class Product(models.Model):
    Product_Name = models.CharField(max_length=200)
    Description = models.TextField()
    Unit_Price = models.IntegerField()
    '''class status(models.TextChoices):  
        BAN_HET='Bán hết','BÁN HẾT'  
        CON_HANG='CÒN HÀNG','Còn hàng'  
    Status= models.CharField(choices=status.choices,max_length=50)'''
    Quantity = models.IntegerField()
    Date_Edited = models.DateField()
    Date_Created = models.DateField()
    Category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    Order = models.ManyToManyField('Order', through='OrderDetail')
    Color = models.TextField()

    def __str__(self):
        return self.Product_Name


# class Cart(models.Model):
# User=models.OneToOneField(Customer,on_delete=models.CASCADE)
# Create_at=models.DateTimeField(auto_now_add=True)
# Updated_at=models.DateTimeField(auto_now_add=True)

class CartItems(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    Subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.User.username} - {self.Product.Product_Name} ({self.Quantity})"


class ProductImage(models.Model):
    Is_Primary = models.BooleanField()
    Image_Url = models.URLField(max_length=50)
    Alt_Text = models.TextField()
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)


class OrderDetail(models.Model):
    Order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderdetail')
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    Subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Tính Subtotal từ Unit_Price * Quantity mỗi khi OrderDetail được lưu.
        """
        # Tính Subtotal nếu chưa có giá trị
        if not self.Subtotal or self.Subtotal:
            self.Subtotal = self.Product.Unit_Price * self.Quantity
        super().save(*args, **kwargs)  # Lưu đối tượng sau khi tính Subtotal


class ReviewProduct(models.Model):
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    Rating = models.IntegerField()
    Content = models.TextField()
    Date_Created = models.DateField()
    Date_Edited = models.DateTimeField(auto_now=True, null=True)
    Order_Detail = models.OneToOneField(OrderDetail, on_delete=models.CASCADE)