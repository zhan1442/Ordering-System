from django import forms
from .models import Order, Drug, Product
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset
from crispy_forms.bootstrap import PrependedText, FormActions, StrictButton


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    # The type is 'password' to hide the input
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Password', 'type': 'password'}))


class OrderStatus_Form(forms.Form):

    status = forms.ChoiceField(
        widget=forms.RadioSelect, choices=Order.ORDER_STATUS_CHOICES, required=True, label='')

    fields = [
        "status",
    ]


class Drug_form(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = Drug
        fields = ['brand', 'name', 'strength', 'quantity', ]

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-inline'
    helper.field_template = 'bootstrap3/layout/inline_field.html'
    helper.layout = Layout(
        'brand',
        'name',
        'strength',
        'quantity',
        FormActions(StrictButton('Create', type="submit")),
    )


class Product_form(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['brand', 'name', 'strength', 'price', 'CIN', 'description', ]

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-sm-4'
    helper.field_class = 'col-sm-5'

    helper.layout = Layout(
        Fieldset('Product Tag',
                 'brand',
                 'name',),
        Fieldset('Product Info',
                 'strength',
                 PrependedText('price', '$'),
                 'CIN',),
        Fieldset('Description',
                 Field('description', rows=3),),
        FormActions(StrictButton('Submit', type="submit", css_class='btn-default', style="margin-left: 120px;")),
    )
