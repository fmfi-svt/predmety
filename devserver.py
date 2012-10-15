#!/usr/bin/env python

try:
    import predmety.local_settings as settings
except ImportError:
    import predmety.settings as settings

from predmety.app import PredmetyApp
application = PredmetyApp(settings=settings)

if __name__ == '__main__':
    import os
    from werkzeug.serving import run_simple
    from predmety.app import wrap_static
    run_simple('127.0.0.1', os.getenv('PORT') or 5000,
               wrap_static(application), use_debugger=True,
               use_reloader=True)

