from django.shortcuts import render, get_object_or_404, redirect
from Webtote.models import Order, OrderDetail, Customer
from datetime import date
from .forms import CancelOrderForm, ReturnOrderForm
from django.contrib import messages
def order_list_view(request):
    superuser = request.user.is_superuser
    customer_id = Customer.objects.get(UserName=request.user.username).id or None
    return render(request, 'order_list.html', {
        'customer_id': customer_id,
        'superuser': superuser,
    })


def order_detail(request, order_id):
    order = get_object_or_404(Order, Order_ID=order_id)

    form_cancel, form_return = None, None

    if order.Order_Status == order.OrderStatus.DON_HANG_MOI:
        if request.method == "POST" and "cancel-btn" in request.POST:
            form_cancel = CancelOrderForm(request.POST, instance=order)
            if form_cancel.is_valid():
                form_cancel.save()
                order.Order_Status = order.OrderStatus.DA_HUY
                order.Cancel_Date = date.today()  # Gán ngày hủy
                order.save()  # Lưu lại đối tượng sau khi cập nhật
                messages.success(request, f"Đơn hàng #{order_id} được hủy thành công!")
                return redirect("order_detail", order_id=order_id)
            else:
                messages.error(request, "Lỗi không thể hủy đơn hàng!")
                print(form_cancel.errors)  # Kiểm tra lỗi ở đây
        else:
            form_cancel = CancelOrderForm(instance=order)

    elif order.Order_Status == order.OrderStatus.GIAO_THANH_CONG:
        if request.method == "POST" and "return-btn" in request.POST:
            form_return = ReturnOrderForm(request.POST, instance=order)
            if form_return.is_valid():
                order = form_return.save(commit=False)
                order.Order_Status = order.OrderStatus.HOAN_TRA
                order.Return_Date = date.today()
                order.save()
                messages.success(request, f"Yêu cầu hoàn trả được thông qua!")
                return redirect("order_detail", order_id=order_id)
            else:
                messages.error(request, "Yêu cầu hoàn trả không được thông qua!")
        else:
            form_return = ReturnOrderForm(instance=order)

    return render(
        request,
        "order_detail.html",
        {
            "order": order,
            "form_cancel": form_cancel,
            "form_return": form_return,
            "order_id": order_id,
        },
    )

from django.http import JsonResponse

def confirm_order(request, order_id):
    if request.method == 'POST':
        try:
            order = Order.objects.get(Order_ID=order_id)  # Tìm đơn hàng theo ID
            order.Order_Status = Order.OrderStatus.DA_XAC_NHAN  # Cập nhật trạng thái đơn hàng
            order.save()  # Lưu thay đổi vào cơ sở dữ liệu
            return JsonResponse({'success': True, 'Order_Status': order.Order_Status})  # Trả về thông tin cập nhật
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Order not found'}, status=404)
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)






