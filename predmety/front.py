
# -*- coding: utf-8 -*-

from werkzeug.routing import Rule
from jinja2 import Markup
from .util import layout

def home(request):
    return layout(request, title=u'Vitaj', body=u'Vitaj u nás, drahý návštevník!') 

def not_found(request):
    response = layout(request, title=u'Chyba 404', body=u'Stránka nenajdená...')
    response.status_code = 404
    return response

views = {
    'home': home,
    'not_found': not_found,
}

def get_routes():
    yield Rule('/', methods=['GET'], endpoint=home)



