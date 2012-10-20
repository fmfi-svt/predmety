
from __future__ import division, absolute_import

import os
from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.contrib.sessions import FilesystemSessionStore
from werkzeug.routing import Map, BaseConverter
from werkzeug.exceptions import HTTPException, NotFound
import jinja2
from sqlalchemy.orm import sessionmaker
from . import models

from . import front, go
site_modules = [front, go]

class PredmetyApp(object):
    def __init__(self, settings):
        self.settings = settings

        loader = jinja2.PackageLoader(__package__)
        def guess_autoescape(template_name):
            return template_name and any(template_name.endswith(ext)
                for ext in ('.html', '.htm', '.xml'))
        self.jinja = jinja2.Environment(loader=loader,
                                        autoescape=guess_autoescape)

        self.session_store = FilesystemSessionStore(
            renew_missing=True, path=settings.session_path)

        self.views = {}
        for module in site_modules:
            self.views.update(module.views)
        self.url_map = Map()
        self.url_map.converters['regex'] = RegexConverter
        for module in site_modules:
            for rulefactory in module.get_routes():
                self.url_map.add(rulefactory)

        self.db_engine = settings.db_connect()
        self.DbSession = sessionmaker(bind=self.db_engine)

    def create_tables(self):
        models.create_tables(self.db_engine)

    def render(self, template_name, **context):
        template = self.jinja.get_template(template_name)
        return jinja2.Markup(template.render(context))

    def dispatch_request(self, request):
        try:
            endpoint, values = request.url_adapter.match()
            return endpoint(request, **values)
        except NotFound as e:
            return self.views['not_found'](request)
        except HttpException as e:
            return e

    @Request.application
    def wsgi_app(self, request):
        request.app = self

        request.max_content_length = 16 * 1024 * 1024
        request.max_form_memory_size = 2 * 1024 * 1024

        cookie_name = self.settings.cookie_name
        sid = request.cookies.get(cookie_name, '')
        request.session = self.session_store.get(sid)

        request.db_session = self.DbSession()

        request.url_adapter = self.url_map.bind_to_environ(request.environ)

        def build_url(view_name, *args, **kwargs):
            endpoint = self.views[view_name]
            return request.url_adapter.build(endpoint, *args, **kwargs)
        request.build_url = build_url

        response = self.dispatch_request(request)

        if request.session.should_save:
            self.session_store.save(request.session)
            response.set_cookie(cookie_name, request.session.sid)
        elif sid and request.session.new and hasattr(response, 'delete_cookie'):
            response.delete_cookie(cookie_name)

        request.db_session.close()

        return response

    def __call__(self, *args):
        return self.wsgi_app(*args)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

def wrap_static(app):
    return SharedDataMiddleware(app, {
        '/static': os.path.join(os.path.dirname(__file__), 'static')
    })

