from django import forms
from Webtote.models import DeliveryInformation, PaymentMethod, ShipmentMethod, Discount


class CheckoutForm(forms.Form):
    Name = forms.CharField(label="Tên người nhận", max_length=250)
    Phone_Number = forms.CharField(label="Số điện thoại", max_length=15)
    Address = forms.CharField(label="Địa chỉ giao hàng", widget=forms.Textarea)

    Payment_Method = forms.ModelChoiceField(
        label="Phương thức thanh toán",
        queryset=PaymentMethod.objects.all()
    )
    Shipment_Method = forms.ModelChoiceField(
        label="Phương thức vận chuyển",
        queryset=ShipmentMethod.objects.all()
    )
    Discount_Code = forms.ModelChoiceField(
        label="Discount Code",
        queryset=Discount.objects.all(),
        required=False,
    )
