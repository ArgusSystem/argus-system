import sys


def null_device():
    if sys.platform == 'win32':
        return 'nul'
    else:
        return '/dev/null'
