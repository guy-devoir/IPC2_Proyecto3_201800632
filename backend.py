import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    try:
        pass
    except ImportError as exc:
        raise ImportError

if __name__ == '__main__':
    main()