from django import forms
from .models import Order, Drug


class OrderStatus_Form(forms.Form):

    status = forms.ChoiceField(
        widget=forms.RadioSelect, choices=Order.ORDER_STATUS_CHOICES, required=True, label='')

    fields = [
        "status",
    ]


class Drug_form(forms.ModelForm):

    class Meta:
        model = Drug
        fields = ["brand", "name", 'strength', 'quantity', ]
