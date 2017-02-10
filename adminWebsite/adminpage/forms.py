from django import forms
from .models import Order


class OrderStatus_Form(forms.Form):

    status = forms.ChoiceField(
        widget=forms.RadioSelect, choices=Order.ORDER_STATUS_CHOICES, required=True, label='')

    fields = [
        "status",
    ]
