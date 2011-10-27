from django.forms import ModelForm, widgets
from contact.models import Contact

class ContactForm(ModelForm):

    class Meta:
        model = Contact
        widgets = {
            'name':widgets.TextInput(), 
            'email':widgets.TextInput(),
            'subject':widgets.TextInput(),
            'message':widgets.Textarea(),
        }