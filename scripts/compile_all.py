import py_compile
import sys
from pathlib import Path

errors = []
for p in Path('.').rglob('*.py'):
    try:
        py_compile.compile(str(p), doraise=True)
    except py_compile.PyCompileError as e:
        errors.append((str(p), e.exc_value))

if not errors:
    print('All files compiled successfully')
    sys.exit(0)

for f, err in errors:
    print('File:', f)
    print(err)
    print('-'*60)

sys.exit(2)
