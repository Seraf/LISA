#!/usr/bin/env python
import os
import sys
from os import environ
from os.path import dirname, abspath
from django.core.management import execute_from_command_line
from web import weblisa, googlespeech, manageplugins, interface

if __name__ == "__main__":
    sys.path.append(os.path.normpath(os.path.join(os.path.abspath("."), "web")))
    sys.path.append(os.path.normpath(os.path.join(os.path.abspath("."), "web/weblisa")))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weblisa.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
