from django import forms
from .models import Client,Order,Drug
from django.forms.formsets import BaseFormSet

class ClientForm(forms.ModelForm):
    class Meta:
        model=Client
        fields=[
            "client_name",
            "phone_number",
            "contact_email"
        ]

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "comment"
        ]


class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = [
            "name",
            "brand",
            "quantity",
            "strength"
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Drug Name'}),
            'brand': forms.TextInput(attrs={'placeholder': 'Drug Brand'}),
            'quantity': forms.TextInput(attrs={'placeholder': 'Quantity'}),
            'strength': forms.TextInput(attrs={'placeholder': 'Strength'}),
        }



class BaseDrugFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        names = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                name = form.cleaned_data['name']
                if name:
                    if name in names:
                        duplicates = True
                    names.append(name)

                if duplicates:
                    raise forms.ValidationError(
                        'Please fill in a drug form with different drugs.',
                        code='duplicate_drugs'
                    )

