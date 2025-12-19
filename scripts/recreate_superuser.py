import os

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
    import django
    django.setup()
    from accounts.models import User

    # Delete existing superusers
    deleted_count, _ = User.objects.filter(is_superuser=True).delete()
    print(f"Deleted {deleted_count} existing superuser(s).")

    print("To create a new superuser, run the following command interactively:")
    print("python manage.py createsuperuser")

except Exception as e:
    print('ERROR:', repr(e))
