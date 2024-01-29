import os
import sys
from pathlib import Path

import django
from django.core.wsgi import get_wsgi_application


def configure_django():
    PROJECT_ROOT_DIR = Path(os.path.abspath(__file__)).parents[1]
    DJANGO_ROOT_DIR = PROJECT_ROOT_DIR / "storm_incidents"
    sys.path.append(DJANGO_ROOT_DIR.as_posix())
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "storm_incidents.settings"
    )

    django.setup()
