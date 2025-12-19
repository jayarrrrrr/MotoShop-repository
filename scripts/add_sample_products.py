import os
from io import BytesIO
from PIL import Image

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
    import django
    django.setup()
    from products.models import Product, Category
    from accounts.models import VendorProfile, User
    from django.core.files.base import ContentFile

    # Create sample categories if they don't exist
    categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden']
    for cat_name in categories:
        Category.objects.get_or_create(name=cat_name)

    # Get or create a vendor
    user, created = User.objects.get_or_create(
        username='sample_vendor',
        defaults={
            'email': 'vendor@example.com',
            'first_name': 'Sample',
            'last_name': 'Vendor'
        }
    )
    if created:
        user.set_password('password123')
        user.save()

    # Sample products data
    products_data = [
        {
            'name': 'Wireless Headphones',
            'description': 'High-quality wireless headphones with noise cancellation.',
            'price': 99.99,
            'stock': 50,
            'category': 'Electronics'
        },
        {
            'name': 'Cotton T-Shirt',
            'description': 'Comfortable cotton t-shirt available in multiple colors.',
            'price': 19.99,
            'stock': 100,
            'category': 'Clothing'
        },
        {
            'name': 'Python Programming Book',
            'description': 'Comprehensive guide to Python programming.',
            'price': 39.99,
            'stock': 30,
            'category': 'Books'
        },
        {
            'name': 'Garden Tools Set',
            'description': 'Complete set of essential garden tools.',
            'price': 49.99,
            'stock': 20,
            'category': 'Home & Garden'
        },
        {
            'name': 'Smartphone Case',
            'description': 'Protective case for smartphones.',
            'price': 14.99,
            'stock': 75,
            'category': 'Electronics'
        },
        {
            'name': 'Running Shoes',
            'description': 'Comfortable running shoes for all terrains.',
            'price': 79.99,
            'stock': 40,
            'category': 'Clothing'
        }
    ]

    # Create products with placeholder images
    for i, product_data in enumerate(products_data):
        category = Category.objects.get(name=product_data['category'])

        # Create a placeholder image
        img = Image.new('RGB', (400, 300), color=(73, 109, 137))
        img_buffer = BytesIO()
        img.save(img_buffer, format='JPEG')
        img_buffer.seek(0)

        product = Product.objects.create(
            vendor=vendor,
            category=category,
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            stock=product_data['stock']
        )

        # Save the image
        product.image.save(f'product_{i+1}.jpg', ContentFile(img_buffer.getvalue()), save=True)

        print(f"Created product: {product.name}")

    print("Sample products added successfully!")

except Exception as e:
    print('ERROR:', repr(e))
