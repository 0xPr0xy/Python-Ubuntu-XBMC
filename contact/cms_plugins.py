from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase, CMSPlugin
from django.utils.translation import ugettext_lazy as _
from contact.models import Contact
from contact.forms import ContactForm
from django.conf import settings
from django.contrib import messages

class ContactPlugin(CMSPluginBase):
    """Enables latest event to be rendered in CMS"""

    model = CMSPlugin
    name = "Form: Contact"
    render_template = "cms/plugins/contactplugin.html"
    admin_preview = False

    def render(self, context, instance, placeholder):
        request = context['request']
        if request.method == "POST":
            form = ContactForm(request.POST)
            if form.is_valid():                
                form.save()
                messages.info(request, "Bedankt voor uw bericht.")
            else:
                messages.info(request, "U heeft niet alle velden correct ingevuld.")
        form = ContactForm()
        context.update({
        'contact': instance,
        'form': form,
            })
        return context
    
plugin_pool.register_plugin(ContactPlugin)