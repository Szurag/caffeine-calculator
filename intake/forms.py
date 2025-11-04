from django import forms
from intake.models import Intake
from products.models import Product


class IntakeForm(forms.ModelForm):
    class Meta:
        model = Intake
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control',
                'id': 'product-select'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1',
                'placeholder': 'Wprowadź ilość (np. 1, 2, 3...)'
            })
        }
        labels = {
            'product': 'Produkt',
            'quantity': 'Ilość'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['product'].queryset = Product.objects.filter(
                is_global=True
            ) | Product.objects.filter(created_by=user)
        else:
            self.fields['product'].queryset = Product.objects.filter(is_global=True)

