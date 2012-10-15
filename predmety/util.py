
from werkzeug.wrappers import Response


def flash(request, type, message):
    flashes = request.session.setdefault('flash', {})
    this_type = flashes.setdefault(type, [])
    this_type.append(message)


def response(body):
    return Response(body, content_type='text/html; charset=UTF-8')


def layout(request, **orig_context):
    app = request.app
    settings = app.settings
    def get_flash():
        # ModificationTrackingDict considers 'pop' a modification even
        # if the key didn't exist, so we check that first
        if not request.session.has_key('flash'): return {}
        return request.session.pop('flash')
    context = {
        'static_url': request.script_root + '/static/',
        'get_flash': get_flash
    }
    context.update(orig_context)
    return response(request.app.render('layout.html', **context))

