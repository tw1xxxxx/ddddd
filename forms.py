from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class ClothesForm(forms.ModelForm):
    class Meta:
        model = Clothes
        fields = ['name', 'description', 'price', 'color', 'min_size', 'max_size', 'photo', 'is_exists', 'collection', 'category']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']



class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'description']


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'country', 'description', 'logo']
        widgets = {
            'logo': forms.FileInput(attrs={'class': 'form-control form-control-lg', 'accept': 'image/*'}),
        }

class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ['brand', 'name']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким именем уже существует.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CarForm(forms.ModelForm):
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=True, label='Марка')
    year = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'type': 'number',
            'class': 'form-control form-control-lg',
            'min': '1900',
            'max': '2024',
            'step': '1'
        }),
        label='Год выпуска'
    )

    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'price', 'image', 'features', 'vin', 'color', 'mileage', 'is_available']
        widgets = {
            'model': forms.Select(attrs={'class': 'form-control form-control-lg'}),
            'image': forms.FileInput(attrs={'class': 'form-control form-control-lg', 'accept': 'image/*'}),
            'price': forms.NumberInput(attrs={'class': 'form-control form-control-lg'}),
            'year': forms.NumberInput(attrs={'class': 'form-control form-control-lg'}),
            'brand': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'features': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows': 3}),
            'vin': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'color': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control form-control-lg'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].queryset = Model.objects.none()

        if self.instance and self.instance.pk:
            self.fields['brand'].initial = self.instance.model.brand.id
            self.fields['model'].queryset = Model.objects.filter(brand=self.instance.model.brand)
            self.fields['model'].initial = self.instance.model.id
            self.fields['price'].initial = self.instance.price
            self.fields['year'].initial = self.instance.year
            self.fields['image'].initial = self.instance.image
            self.fields['features'].initial = self.instance.features
            self.fields['vin'].initial = self.instance.vin
            self.fields['color'].initial = self.instance.color
            self.fields['mileage'].initial = self.instance.mileage
            self.fields['is_available'].initial = self.instance.is_available
        elif 'brand' in self.data:
            try:
                brand_id = int(self.data.get('brand'))
                self.fields['model'].queryset = Model.objects.filter(brand_id=brand_id)
            except (ValueError, TypeError):
                pass

class CustomerForm(forms.ModelForm):
    email = forms.EmailField(label='Email')
    is_staff = forms.BooleanField(
        label='Права администратора',
        required=False,
        help_text='Установите флажок, чтобы предоставить права администратора'
    )

    class Meta:
        model = Customer
        fields = ['email', 'phone', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
            self.fields['is_staff'].initial = self.instance.user.is_staff

    def save(self, commit=True):
        customer = super().save(commit=False)
        if customer.user:
            customer.user.email = self.cleaned_data['email']
            customer.user.is_staff = self.cleaned_data['is_staff']
            customer.user.save()
        if commit:
            customer.save()
        return customer

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'position', 'phone', 'email', 'photo']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['car', 'customer', 'employee', 'price', 'sale_date']
        widgets = {
            'sale_date': forms.DateInput(attrs={'type': 'date'}),
            'employee': forms.Select(attrs={'class': 'form-select form-select-lg'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].queryset = User.objects.filter(is_staff=True)

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'duration']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['customer', 'car', 'rating', 'text']

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['car']

class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['car']

class TestDriveForm(forms.ModelForm):
    class Meta:
        model = TestDrive
        fields = ['date']
        widgets = {
            'date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control form-control-lg',
                'min': '2024-01-01T00:00',
                'max': '2025-12-31T23:59'
            }),
        }


