from django.shortcuts import render, redirect
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from django.utils import timezone
from uuid import uuid4
from django.contrib.auth.decorators import login_required


def cart_view(request):
	cart = None
	if request.user.is_authenticated:
		cart, _ = Cart.objects.get_or_create(user=request.user)
		if request.method == 'POST':
			product_id = request.POST.get('product_id')
			quantity = request.POST.get('quantity')
			remove = request.POST.get('remove')
			if product_id:
				try:
					product = Product.objects.get(id=product_id)
					# Remove item from cart
					if remove:
						CartItem.objects.filter(cart=cart, product=product).delete()
					# Update quantity if provided
					elif quantity is not None:
						try:
							qty = int(quantity)
						except (ValueError, TypeError):
							qty = 1
						if qty <= 0:
							CartItem.objects.filter(cart=cart, product=product).delete()
						else:
							cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
							cart_item.quantity = qty
							cart_item.save()
					# Default: add one if no quantity/remove provided
					else:
						cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
						if not created:
							cart_item.quantity += 1
							cart_item.save()
				except Product.DoesNotExist:
					pass
			return redirect('cart_view')
	return render(request, 'orders/cart.html', {'cart': cart})


def checkout(request):
	# Ensure cart is available for rendering
	cart = None
	if request.user.is_authenticated:
		cart, _ = Cart.objects.get_or_create(user=request.user)

	# Handle order placement on POST
	if request.method == 'POST':
		if not request.user.is_authenticated:
			return redirect('login')

		if not cart or not cart.items.exists():
			return redirect('cart_view')

		# collect shipping info
		first = request.POST.get('first_name', '').strip()
		last = request.POST.get('last_name', '').strip()
		address = request.POST.get('address', '').strip()
		city = request.POST.get('city', '').strip()
		state = request.POST.get('state', '').strip()
		zipc = request.POST.get('zip', '').strip()

		# validate required fields
		required = {
			'First name': first,
			'Last name': last,
			'Address': address,
			'City': city,
			'State': state,
			'ZIP': zipc,
		}
		missing = [k for k, v in required.items() if not v]
		if missing:
			error = 'Please fill in required fields: ' + ', '.join(missing)
			form_values = {
				'first_name': first,
				'last_name': last,
				'address': address,
				'city': city,
				'state': state,
				'zip': zipc,
			}
			return render(request, 'orders/checkout.html', {
				'cart': cart,
				'error': error,
				'form': form_values,
			})

		shipping_address = f"{first} {last}\n{address}\n{city}, {state} {zipc}".strip()

		# create order
		order_number = uuid4().hex[:12].upper()
		total = cart.get_total()

		order = Order.objects.create(
			user=request.user,
			order_number=order_number,
			total_amount=total,
			shipping_address=shipping_address,
		)

		# create order items
		for item in cart.items.all():
			OrderItem.objects.create(
				order=order,
				product=item.product,
				vendor=getattr(item.product, 'vendor', None),
				quantity=item.quantity,
				price=item.product.price,
			)

		# clear cart
		cart.items.all().delete()

		return redirect('order_success', order_number=order.order_number)

	return render(request, 'orders/checkout.html', {'cart': cart})


def order_success(request, order_number):
	try:
		order = Order.objects.get(order_number=order_number)
	except Order.DoesNotExist:
		return redirect('product_list')
	return render(request, 'orders/order_success.html', {'order': order})


@login_required
def my_orders(request):
	# list orders for the current user
	orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
	return render(request, 'orders/my_orders.html', {'orders': orders})


def buy_now(request):
	# Create/replace the user's cart with a single product then go to checkout
	if not request.user.is_authenticated:
		return redirect('login')

	if request.method == 'POST':
		product_id = request.POST.get('product_id')
		quantity = request.POST.get('quantity') or 1
		try:
			product = Product.objects.get(id=product_id)
		except (Product.DoesNotExist, TypeError, ValueError):
			return redirect('product_list')

		cart, _ = Cart.objects.get_or_create(user=request.user)
		# remove existing items and add this one
		cart.items.all().delete()
		try:
			qty = int(quantity)
		except (ValueError, TypeError):
			qty = 1
		if qty <= 0:
			qty = 1

		CartItem.objects.create(cart=cart, product=product, quantity=qty)
		return redirect('checkout')

	return redirect('product_list')
