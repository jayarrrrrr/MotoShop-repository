import importlib, inspect, sys, pathlib
# ensure project root is on sys.path when running this script from /scripts
ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

m = importlib.import_module('accounts.models')
print('module:', m)
print('module.__file__:', getattr(m, '__file__', None))
print('classes defined in module:')
for name,obj in inspect.getmembers(m, inspect.isclass):
    if obj.__module__ == m.__name__:
        print(' -', name)
print('\nall names:')
print([n for n in dir(m) if not n.startswith('_')])
print('\nsource:\n')
import inspect
print(inspect.getsource(m))
