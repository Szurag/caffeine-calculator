from django import forms
from products.models import Product


class AddProductForm(forms.ModelForm):
    photo = forms.ImageField(required=False, label='Zdjęcie produktu (opcjonalne)')

    class Meta:
        model = Product
        fields = ['name', 'caffeine_mg']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Wprowadź nazwę produktu'
            }),
            'caffeine_mg': forms.NumberInput(attrs={
                'min': '0',
                'step': '0.01',
                'placeholder': 'Wprowadź ilość kofeiny w mg'
            })
        }
        labels = {
            'name': 'Nazwa produktu',
            'caffeine_mg': 'Ilość kofeiny (mg)'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_caffeine_mg(self):
        caffeine_mg = self.cleaned_data.get('caffeine_mg')
        if caffeine_mg is not None and caffeine_mg < 0:
            raise forms.ValidationError("Ilość kofeiny nie może być ujemna.")
        return caffeine_mg

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Nazwa produktu jest wymagana.")
        return name

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            if photo.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Plik jest zbyt duży. Maksymalny rozmiar to 5MB.")

            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            ext = photo.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError(
                    f"Niedozwolone rozszerzenie pliku. Dozwolone: {', '.join(allowed_extensions)}"
                )

        return photo
