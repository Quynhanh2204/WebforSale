from django import forms
from Webtote.models import Order

class CancelOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['Reason']
        widgets = {
            'Reason': forms.Select(
                choices=Order.CANCEL_REASONS,
                attrs={'class': 'form-control'}
            ),
        }

class ReturnOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['Return_Reason']
        widgets = {
            'Return_Reason': forms.Select(
                choices=Order.RETURN_REASONS,
                attrs={'class': 'form-control'}
            ),
        }
