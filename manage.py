#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    # Proje adın 'core_project' olduğu için burası böyle kalmalı
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django kütüphanesi bulunamadı. venv aktif mi?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()