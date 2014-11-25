#!/usr/bin/env python

import os
from os.path import normpath, dirname, abspath
import sys

if __name__ == "__main__":
    # Insert PYTHONPATH relative to manage.py
    parent_dir = normpath(dirname(dirname(abspath(__file__))))
    sys.path.append(parent_dir)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rekishi.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
