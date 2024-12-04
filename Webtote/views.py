import Cart
from Cart.context_processors import cart_item_count
from .models import *
from django.contrib.auth.forms import AuthenticationForm

from .forms import CustomUserChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import  CustomUserCreationForm
from .models import Customer
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


@login_required
def user_profile(request):
    # Giả sử bạn có mô hình Order và muốn lấy lịch sử mua hàng của người dùng
    return render(request, 'customer_profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'customer_profile_edit.html', {'form': form})

@never_cache
def logout_view(request):
    logout(request)
    return render(request, 'logout.html')

# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()  # Lưu người dùng mới vào cơ sở dữ liệu
#             Customer.objects.create(
#                 Name=form.cleaned_data['last_name'] + " " + form.cleaned_data['first_name'],
#                 UserName=form.cleaned_data['username'],
#                 Password=form.cleaned_data['password1'],
#                 Email=form.cleaned_data['email'],
#             )
#             messages.success(request, "Tạo tài khoản thành công!")
#             return redirect('login')  # Chuyển hướng người dùng đến trang đăng nhập
#         else:
#             messages.error(request, "Có lỗi trong quá trình đăng ký.")
#     else:
#         form = CustomUserCreationForm()
#
#     return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            #customer = Customer.objects.get(UserName=form.cleaned_data['username'])
            cart_items = CartItems.objects.filter(User=user)
            cart_items_count = sum(i.Quantity for i in cart_items)
            request.session['cart_count'] = cart_items_count

            messages.success(request, 'Đăng nhập thành công.')
            # next_page = request.POST.get('next', '/')  # Chuyển hướng người dùng sau khi đăng nhập
            return redirect(base)
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng..")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             messages.success(request, 'Đăng nhập thành công.')
#             # next_page = request.POST.get('next', '/')  # Chuyển hướng người dùng sau khi đăng nhập
#             return redirect(base)
#         else:
#             messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng..")
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Lưu người dùng mới vào cơ sở dữ liệu
            messages.success(request, "Tạo tài khoản thành công!")
            return redirect('login')  # Chuyển hướng người dùng đến trang đăng nhập
        else:
            messages.error(request, "Có lỗi trong quá trình đăng ký.")
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})
def base (request):
    return render(request, 'homepage.html')
def csdoi_tra(request):
    return render(request, 'csdoi_tra.html')
def csthanh_toan(request):
    return render(request, 'csthanh_toan.html')
def csgiao_hang(request):
    return render(request, 'csgiao_hang.html')
def hd_mua(request):
    return render(request, 'hd_mua.html')

