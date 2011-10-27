from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from os.path import join

def mail(request):
    if request.method == 'POST':
        
        user_name = request.POST.get('user_name')
        friend_name = request.POST.get('friend_name')
        user_email = request.POST.get('user_email')
        friend_email = request.POST.get('friend_email')

        if user_email and friend_email and user_name and friend_name:

            subject = join('Mail van ' + user_name)
            first_link = '' #html link
            second_link = '' #html link
            message = join('') #message with links
            htmlmessage = message
            html = '<html><body>' + htmlmessage + '</body></html>'
            mail = EmailMultiAlternatives(subject, message, user_email, [friend_email])
            mail.attach_alternative(html, "text/html")
            
            if subject and message and first_link and second_link:
                try:
                    mail.send()
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return HttpResponseRedirect('/mail/success')
            else:
                return HttpResponse('Make sure all fields are entered and valid.')
        else:
            return HttpResponse('Make sure all fields are entered and valid.')
    else:
        return HttpResponse('Current request method is not a POST.')
        
def success(request):
    return HttpResponse('Mail successfully sent')