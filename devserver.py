#!/usr/bin/env python

try:
    import predmety.local_settings as settings
except ImportError:
    import predmety.settings as settings

from predmety.app import PredmetyApp
application = PredmetyApp(settings=settings)

if __name__ == '__main__':
    import os
    import sys
    from werkzeug.serving import run_simple
    from predmety.app import wrap_static

    if sys.argv[1:] == []:
        run_simple('127.0.0.1', os.getenv('PORT') or 5000,
                   wrap_static(application), use_debugger=True,
                   use_reloader=True)
    elif sys.argv[1:] == ['create-tables']:
        application.create_tables()
    else:
        raise ValueError('bad args')
