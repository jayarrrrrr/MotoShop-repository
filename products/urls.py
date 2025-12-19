from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.vendor_add_product, name='vendor_add_product'),
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor/<int:pk>/edit/', views.vendor_edit_product, name='vendor_edit_product'),
    path('vendor/<int:pk>/delete/', views.vendor_delete_product, name='vendor_delete_product'),
    path('', views.product_list, name='product_list'),
    path('admin/add/', views.admin_add_product, name='admin_add_product'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
]
