from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from itertools import chain
from contact.forms import ContactForm 
from contact.models import Contact

# Create your views here.
def index(request):
   
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['subscribe']:   
                form.save()
                return render_to_response('amsterdamstore.html', mimetype='text/html', context_instance=RequestContext(request))
    #return default store
    return render_to_response('amsterdamstore.html', mimetype='text/html', context_instance=RequestContext(request))
    
