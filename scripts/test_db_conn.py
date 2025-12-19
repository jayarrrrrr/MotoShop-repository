from pathlib import Path
import pymysql

# Load DATABASES from settings.py without configuring Django
settings_path = Path(__file__).resolve().parents[1] / 'ecommerce' / 'settings.py'
src = settings_path.read_text(encoding='utf-8')
ns = {'__file__': str(settings_path)}
exec(compile(src, str(settings_path), 'exec'), ns)
db = ns.get('DATABASES', {}).get('default', {})

host = db.get('HOST', 'localhost')
port = int(db.get('PORT', 3306))
user = db.get('USER')
password = db.get('PASSWORD')

print('Configured DB user:', user)

def try_connect(u, p):
    try:
        conn = pymysql.connect(host=host, user=u, password=p, port=port)
        conn.close()
        print('SUCCESS:', u)
    except Exception as e:
        print('FAIL:', u, '-', repr(e))

try_connect(user, password)
try_connect('root', '')
