from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from models import Admin
from self.forms import LoginForm

def index(request):
    return auth(request)

def auth(request):
    data_received = request.POST or request.GET
    message = ""
    if data_received:
        form = LoginForm(data_received)
        if form.is_valid():
            #admin = get_object_or_404(Admin, Account=form.cleaned_data['Account'])
            try:
                admin =  Admin.objects.get(Account=form.cleaned_data['Account'])
                request.session['admin'] = admin
                return HttpResponseRedirect(reverse('tees:index'))
            
            #catch doesnotexist error to prevent a 404
            except Admin.DoesNotExist:
                form = LoginForm()
                message = "Account ID Does not exist"
                return render_to_response('auth.html', {'form':form, 'message':message,}, context_instance=RequestContext(request))
        else:
            message = "Invalid Account ID"
    else:
        form = LoginForm()
        
    return render_to_response('auth.html', {'form':form, 'message':message,}, context_instance=RequestContext(request))
