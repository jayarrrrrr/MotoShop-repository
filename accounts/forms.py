from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, VendorProfile, CustomerProfile


class VendorRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username', 'autocomplete': 'username'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Email address', 'autocomplete': 'email'
    }))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Create password', 'autocomplete': 'new-password'
    }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Repeat password', 'autocomplete': 'new-password'
    }))
    shop_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shop name'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'shop_name', 'phone']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.is_vendor = True
        if commit:
            user.save()
            VendorProfile.objects.create(
                user=user,
                shop_name=self.cleaned_data.get('shop_name', '').strip(),
                phone=self.cleaned_data.get('phone', '').strip()
            )
        return user


class CustomerRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username', 'autocomplete': 'username'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Email address', 'autocomplete': 'email'
    }))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Create password', 'autocomplete': 'new-password'
    }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Repeat password', 'autocomplete': 'new-password'
    }))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Street address, city, ZIP'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'address', 'phone']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.is_customer = True
        if commit:
            user.save()
            CustomerProfile.objects.create(
                user=user,
                address=self.cleaned_data.get('address', '').strip(),
                phone=self.cleaned_data.get('phone', '').strip()
            )
        return user


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Username', 'autocomplete': 'username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password', 'autocomplete': 'current-password'
    }))

    pass

    def clean(self):
        cleaned = super().clean()
        return cleaned

