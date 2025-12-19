import os
try:
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
	import django
	django.setup()
	from django.conf import settings
	print('DJANGO settings DB user:', settings.DATABASES['default'].get('USER'))
except Exception as e:
	print('ERROR:', repr(e))
