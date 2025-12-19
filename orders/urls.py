from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/', views.checkout, name='checkout'),
    path('buy-now/', views.buy_now, name='buy_now'),
    path('checkout/success/<str:order_number>/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
]
