import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
import django
django.setup()

from products.models import Category


def create_categories():
    names = [
        'Engine & Performance',
        'Electrical & Lighting',
        'Brakes & Suspension',
        'Wheels & Tires',
        'Transmission & Drivetrain',
        'Body Parts & Frame',
        'Exhaust System',
        'Controls & Cables',
        'Maintenance & Fluids',
        'Accessories',
        'Tools & Garage',
    ]

    created = []
    for name in names:
        obj, was_created = Category.objects.get_or_create(name=name)
        created.append((name, was_created))

    for name, was_created in created:
        print(f"{'Created' if was_created else 'Exists  '}: {name}")


if __name__ == '__main__':
    create_categories()
