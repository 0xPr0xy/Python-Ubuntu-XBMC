from functools import wraps
from django.conf import settings
from django.utils.decorators import available_attrs
from django.http import HttpResponseRedirect

def login_required(view):
    "too view a page you've got to be an admin."
    @wraps(view, assigned=available_attrs(view))
    def _wrapped_view(request, *args, **kwargs):
        if request.session.has_key('admin'):
            return view(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')
    return _wrapped_view
