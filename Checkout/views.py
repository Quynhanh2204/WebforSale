import qrcode
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.template.defaultfilters import floatformat
from django.utils import timezone
from Webtote.models import Order, DeliveryInformation, OrderDetail, Product, ShipmentMethod, PaymentMethod, Discount, \
    CartItems, Customer
from .forms import CheckoutForm
import base64
import locale

# Đặt locale là tiếng Việt
locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')
temp = 0;
def format_currency(value):
    # Định dạng số theo kiểu tiền tệ Việt Nam
    formatted_value = locale.format_string("%d", value, grouping=True)
    # Thêm hậu tố "đ" cho tiền tệ Việt Nam
    return f"{formatted_value} đ"
@login_required
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            # Lấy phương thức vận chuyển và thanh toán
            shipment_method = form.cleaned_data['Shipment_Method']
            payment_method = form.cleaned_data['Payment_Method']

            # Kiểm tra mã giảm giá
            discount_code = form.cleaned_data['Discount_Code']
            discount = None
            discount_value = 0
            temp = discount_value
            if discount_code:
                try:
                    discount = Discount.objects.get(Discount_Code=discount_code, is_active=True)
                    discount_value = discount.Discount_Value / 100
                except Discount.DoesNotExist:
                    messages.error(request, "Mã giảm giá không hợp lệ hoặc đã hết hạn!")
            # Tạo thông tin giao hàng
            customer = Customer.objects.get(UserName=request.user.username)
            delivery_info = DeliveryInformation.objects.create(
                Name=form.cleaned_data['Name'],
                Phone_Number=form.cleaned_data['Phone_Number'],
                Address=form.cleaned_data['Address'],
                Customer=customer
            )

            # Tạo đơn hàng
            order = Order.objects.create(
                Order_Date=timezone.now(),
                Total_Price=0,  # Sẽ cập nhật sau
                Discount=discount,
                Payment_Method=payment_method,
                Shipment_Method=shipment_method,
                Delivery_Infor=delivery_info,
                Customer=customer,
                Order_Status=Order.OrderStatus.DON_HANG_MOI
            )

            cart_items = CartItems.objects.filter(User=request.user)
            total_price = 0
            total_subtotal = 0

            for cart_item in cart_items:
                product = cart_item.Product
                subtotal = cart_item.Subtotal
                total_subtotal += subtotal

                # Tạo chi tiết đơn hàng
                OrderDetail.objects.create(
                    Order=order,
                    Product=product,
                    Quantity=cart_item.Quantity,
                    Subtotal=subtotal
                )
            temp = total_subtotal
            if discount:
                discount_amount = total_subtotal * discount_value
                total_subtotal -= discount_amount
                messages.info(request,
                              f"Đã áp dụng mã giảm giá {discount_code} giảm {discount_amount:.2f}đ")

            # Thêm phí vận chuyển
            total_price = total_subtotal + shipment_method.Method_Cost

            # Cập nhật tổng giá trị đơn hàng
            order.Total_Price = total_price
            order.save()

            #Xoa giỏ hàng sau khi đặt hangf thành công
            cart_items.delete()
            request.session['cart_count'] = 0

            messages.success(request, "Đặt hàng thành công!")
            return redirect('order_confirmation', order_id=order.Order_ID) if payment_method.id == 2 else redirect('vnpay_qr', order_id=order.Order_ID)

    else:
        form = CheckoutForm()

    #customer = Customer.objects.get(UserName=request.user.username)
    cart_items = CartItems.objects.filter(User=request.user)

    # Truyền dữ liệu giỏ hàng và tổng cộng vào template
    total_subtotal = sum(i.Subtotal for i in cart_items)
    context_cart_items = [
        {
            'Quantity': cart_item.Quantity,
            'UnitPrice': cart_item.Product.Unit_Price,
            'ProductName': cart_item.Product.Product_Name,
            'ProductPrimaryImage': cart_item.Product.productimage_set.filter(Is_Primary=True).first()
        } for cart_item in cart_items
    ]

    return render(request, 'checkout.html', {
        'form': form,
        'cart_items': context_cart_items,
        'total_subtotal': format_currency(total_subtotal),
        'total_subtotal_To_Cal': total_subtotal,
        'discount_amount': format_currency(total_subtotal)
    })


@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))



    # Create temporary cart item for checkout
    cart_item = {
        'ProductName': product.Product_Name,
        'Quantity': quantity,
        'UnitPrice': product.Unit_Price,
        'ProductPrimaryImage': product.productimage_set.filter(Is_Primary=True).first()
    }

    total_subtotal = product.Unit_Price * quantity
    shipping_methods = ShipmentMethod.objects.all()
    payment_methods = PaymentMethod.objects.all()
    shipping_cost = shipping_methods.first().Method_Cost if shipping_methods else 0

    context = {
        'cart_items': [cart_item],
        'total_subtotal': total_subtotal,
        'shipping_cost': shipping_cost,
        'total_price': total_subtotal + shipping_cost,
        'form': CheckoutForm(),
        'shipping_methods': shipping_methods,
        'payment_methods': payment_methods
    }

    return render(request, 'checkout.html', context)
def vnpay_qr(request, order_id):
    # Lấy thông tin đơn hàng từ cơ sở dữ liệu
    order = get_object_or_404(Order, Order_ID=order_id)

    # Thông tin thanh toán VNPay (bạn cần tích hợp với hệ thống VNPay của bạn để lấy thông tin này)
    total_amount = order.Total_Price
    order_code = order.Order_ID
    payment_url = f"https://vnpay.vn/checkout?order_id={order_code}&amount={total_amount}"

    # Tạo mã QR từ URL thanh toán VNPay
    qr = qrcode.make(payment_url)

    # Lưu mã QR vào bộ nhớ
    qr_buffer = BytesIO()
    qr.save(qr_buffer, format='PNG')
    qr_base64 = base64.b64encode(qr_buffer.getvalue()).decode('utf-8')

    # Trả về mã QR dưới dạng hình ảnh base64 để hiển thị trong template
    return render(request, 'vnpay_qr.html', {'qr_base64': qr_base64, 'order': order})

def check_discount(request):
    code = request.GET.get('code', '').strip()
    print(f'Nhận mã giảm giá: {code}')  # Kiểm tra mã giảm giá nhận được
    response_data = {
        'valid': False,
        'discount_id': 0,
        'discount_value': 0,
    }

    if code:
        try:
            # Kiểm tra mã giảm giá với điều kiện là mã đang hoạt động
            discount = Discount.objects.get(Discount_Code=code, is_active=True)
            response_data['valid'] = True
            response_data['discount_id'] = discount.id
            response_data['discount_value'] = discount.Discount_Value
            print(f'Mã giảm giá hợp lệ: {discount.Discount_Code}, giảm giá {discount.Discount_Value}%')
        except Discount.DoesNotExist:
            print('Mã giảm giá không hợp lệ hoặc không tồn tại.')

    return JsonResponse(response_data)

def order_confirmation_view(request, order_id):
    order = get_object_or_404(Order, Order_ID=order_id)
    return render(request, 'order_confirmation.html', {'order': order})
