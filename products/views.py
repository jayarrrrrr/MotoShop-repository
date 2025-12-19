from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from .models import Product
from orders.models import Order, OrderItem
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from django.db.models import Q
from .forms import ProductForm
from .forms import VendorProductForm
from django.contrib import messages


def product_list(request):
	query = request.GET.get('q', '').strip()
	products = Product.objects.filter(is_active=True)
	if query:
		# search by name, description or category name
		products = products.filter(
			Q(name__icontains=query) |
			Q(description__icontains=query) |
			Q(category__name__icontains=query)
		).distinct()
	return render(request, 'products/product_list.html', {'products': products, 'query': query})


def product_detail(request, pk):
	product = get_object_or_404(Product, pk=pk, is_active=True)
	return render(request, 'products/product_detail.html', {'product': product})


@user_passes_test(lambda u: u.is_staff)
def admin_add_product(request):
	if request.method == 'POST':
		form = ProductForm(request.POST, request.FILES)
		if form.is_valid():
			product = form.save()
			return redirect(reverse('product_detail', args=[product.pk]))
	else:
		form = ProductForm()

	return render(request, 'products/admin_add_product.html', {'form': form})

@user_passes_test(lambda u: u.is_authenticated and getattr(u, 'is_vendor', False))
def vendor_add_product(request):
	try:
		vendor = request.user.vendorprofile
	except Exception:
		return redirect('product_list')

	if request.method == 'POST':
		form = VendorProductForm(request.POST, request.FILES)
		if form.is_valid():
			product = form.save(commit=False)
			product.vendor = vendor
			product.save()
			return redirect(reverse('product_detail', args=[product.pk]))
	else:
		form = VendorProductForm()

	return render(request, 'products/vendor_add_product.html', {'form': form})


@user_passes_test(lambda u: u.is_authenticated and getattr(u, 'is_vendor', False))
def vendor_dashboard(request):
	try:
		vendor = request.user.vendorprofile
	except Exception:
		return redirect('product_list')

	products = vendor.products.all()

	# Total products
	total_products = products.count()

	# Total sales for this vendor (exclude cancelled orders)
	sales_expr = Sum(ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField(max_digits=12, decimal_places=2)))
	total_sales_agg = OrderItem.objects.filter(vendor=vendor).exclude(order__status='cancelled').aggregate(total=sales_expr)
	total_sales = total_sales_agg.get('total') or 0

	# Total distinct orders containing this vendor's items
	total_orders = Order.objects.filter(items__vendor=vendor).distinct().count()

	# Pending orders for this vendor
	pending_orders = Order.objects.filter(status='pending', items__vendor=vendor).distinct().count()

	context = {
		'products': products,
		'total_products': total_products,
		'total_sales': total_sales,
		'total_orders': total_orders,
		'pending_orders': pending_orders,
	}

	# Hero text for vendor dashboard
	vendor_name = vendor.user.first_name or vendor.shop_name or vendor.user.username
	context.update({
		'vendor_hero': True,
		'hero_title': f'Welcome back, {vendor_name}!',
		'hero_subtitle': 'Manage your products and track your sales',
	})

	return render(request, 'products/vendor_dashboard.html', context)


@user_passes_test(lambda u: u.is_authenticated and getattr(u, 'is_vendor', False))
def vendor_edit_product(request, pk):
	try:
		vendor = request.user.vendorprofile
	except Exception:
		return redirect('product_list')
		

	product = get_object_or_404(Product, pk=pk, vendor=vendor)

	if request.method == 'POST':
		form = VendorProductForm(request.POST, request.FILES, instance=product)
		if form.is_valid():
			form.save()
			messages.success(request, 'ANGIYONG PRODUCT AY NA UPDATE NA ////// EXAMPLE//////.')
			return redirect('vendor_dashboard')
	else:
		form = VendorProductForm(instance=product)

	return render(request, 'products/vendor_edit_product.html', {'form': form, 'product': product})


@user_passes_test(lambda u: u.is_authenticated and getattr(u, 'is_vendor', False))
def vendor_delete_product(request, pk):
	try:
		vendor = request.user.vendorprofile
	except Exception:
		return redirect('product_list')

	product = get_object_or_404(Product, pk=pk, vendor=vendor)

	if request.method == 'POST':
		product.delete()
		messages.success(request, 'Product deleted.')
		return redirect('vendor_dashboard')

	return render(request, 'products/vendor_confirm_delete.html', {'product': product})
