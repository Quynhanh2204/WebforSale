
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from Webtote.models import CartItems, Product , ProductImage, User, Customer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model



@login_required
def cart(request):
    try:
        # Lấy đối tượng 'Customer' của người dùng đã đăng nhập
        #Customer =Customer.objects.filter(UserName=request.user._wrapped.username)
        user = get_object_or_404(User, username=request.user.username)
    except AttributeError:
        return HttpResponse("Bạn cần đăng nhập để xem giỏ hàng của mình.", status=401)

    # Lọc các sản phẩm trong giỏ hàng của khách hàng hiện tại
    cart_items = CartItems.objects.filter(User=user)

    # Tính tổng số lượng và giá trị của các sản phẩm trong giỏ hàng
    total_price = sum(item.Subtotal for item in cart_items)
    total_quantity = sum(item.Quantity for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity
    })

@login_required
def add_to_cart(request, product_id):
    # Kiểm tra nếu yêu cầu là POST
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1)) # Số lượng mặc định là 1 nếu không cung cấp
        #customer = Customer.objects.get(UserName=request.user._wrapped.username)

        added_cart_item = CartItems.objects.create(
            User=request.user,
            Product=product,
            Quantity=quantity,
            Subtotal=product.Unit_Price * quantity
        )

        if added_cart_item:
            current_cart_count = request.session.get('cart_count', {})
            request.session['cart_count'] = current_cart_count + quantity
            return redirect('cart')

    #     # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
    #     if str(product_id) in cart:
    #         cart[str(product_id)]['quantity'] += quantity  # Cộng thêm số lượng vào giỏ hàng
    #     else:
    #         cart[str(product_id)] = {
    #             'name': product.Product_Name,
    #             'price': product.Unit_Price,
    #             'image_url': ProductImage.Image_Url,
    #             'quantity': quantity,
    #         }
    #
    #     request.session['cart'] = cart  # Lưu lại giỏ hàng trong session
    #
    #     # Trả về phản hồi JSON
    #     cart_count = sum(item['quantity'] for item in cart.values())  # Tổng số lượng sản phẩm trong giỏ
    #     return JsonResponse({
    #         'success': True,
    #         'message': f"Đã thêm {product.Product_Name} vào giỏ hàng!",
    #         'cart_count': cart_count,
    #     })
    #
    # return JsonResponse({'success': False, 'message': 'Yêu cầu không hợp lệ!'}, status=400)


def remove_from_cart(request, cart_item_id):
    cart_item = CartItems.objects.get(id=cart_item_id, User=request.user)
    if cart_item:
        current_cart_count = request.session.get('cart_count', {})
        request.session['cart_count'] = current_cart_count - cart_item.Quantity
        cart_item.delete()
        return redirect('cart')


def update_cart_item(request, cart_item_id):
    cart_item = CartItems.objects.get(id=cart_item_id, User=request.user)

    quantity = int(request.POST.get('quantity', 1))
    updated_quantity = cart_item.Quantity + quantity

    current_cart_count = request.session.get('cart_count', {})
    request.session['cart_count'] = current_cart_count + quantity

    if updated_quantity == 0:
        cart_item.delete()
        return redirect('cart')

    product = cart_item.Product
    updated_subtotal = updated_quantity * product.Unit_Price

    cart_item.Quantity = updated_quantity
    cart_item.Subtotal = updated_subtotal
    cart_item.save()

    return redirect('cart')

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.info(request, "Giỏ hàng của bạn trống.")
        return redirect('cart')

    return render(request, 'checkout.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_images = ProductImage.objects.filter(product=product)
    return render(request, 'product_detail.html', {'product': product, 'product_images': product_images})