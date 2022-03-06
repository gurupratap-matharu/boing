import sys

import pgzero

if sys.version_info < (3, 5):
    print(
        "This game requires at least version 3. 5 of Python. Please download"
        "it from www.python.org"
    )
    sys.exit()

pgzero_version = [int(s) for s in pgzero.__version__.split(".")]
if pgzero_version < [1, 2]:
    print(
        "This game requires at least version 1.2 of PyGame Zero. You are"
        "using version {pgzero.__version__}. Please upgrade using the command"
        "'pip install --upgrade pgzero'"
    )
    sys.exit()
