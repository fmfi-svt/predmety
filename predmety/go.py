
from werkzeug.routing import Rule
from werkzeug.utils import redirect
from werkzeug.urls import Href
from werkzeug.exceptions import NotFound
from .models import Link


def go(request, code):
    link = request.db_session.query(Link).get(code)
    if not link: raise NotFound()
    return redirect(link.redirect)


def infosheet(request, code):
    url = Href('https://fajr.fmph.uniba.sk/predmety/informacny-list')(code=code)
    return redirect(url)


views = {
    'go': go,
    'infosheet': infosheet,
}

def get_routes():
    yield Rule('/<code>', methods=['GET'], endpoint=go)
    yield Rule('/<code>/il', methods=['GET'], endpoint=infosheet)
