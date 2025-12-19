from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import VendorRegisterForm, CustomerRegisterForm, LoginForm
from django.contrib import messages
from .models import VendorProfile, CustomerProfile, User


def vendor_register(request): 
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        if request.user.is_vendor:
            return redirect('vendor_dashboard')
        return redirect('product_list')

    if request.method == 'POST':
        form = VendorRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_vendor = True
                user.save()

                VendorProfile.objects.create(
                    user=user,
                    shop_name=form.cleaned_data['shop_name'],
                    phone=form.cleaned_data['phone'],
                )

                login(request, user)
                return redirect('vendor_dashboard')
            except Exception as e:
                messages.error(request, f"Registration failed: {e}")
        else:
            messages.error(request, form.errors.as_text())
    else:
        form = VendorRegisterForm()
    
    return render(request, 'accounts/vendor_register.html', {'form': form})


def customer_register(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        if request.user.is_vendor:
            return redirect('vendor_dashboard')
        return redirect('product_list')

    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_customer = True
                user.save()

                CustomerProfile.objects.create(
                    user=user,
                    address=form.cleaned_data['address'],
                    phone=form.cleaned_data['phone'],
                )

                login(request, user)
                return redirect('product_list')
            except Exception as e:
                messages.error(request, f"Registration failed: {e}")
        else:
            messages.error(request, form.errors.as_text())
    else:
        form = CustomerRegisterForm()

    return render(request, 'accounts/customer_register.html', {'form': form})


def login_user(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        if request.user.is_vendor:
            return redirect('vendor_dashboard')
        return redirect('product_list')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_vendor:
                    return redirect('vendor_dashboard')
                else:
                    return redirect('product_list')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('/accounts/login/')
