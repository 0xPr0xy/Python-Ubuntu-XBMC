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
        score = str(request.POST.get('score'))

        if user_email and friend_email and user_name and friend_name and score:

            subject = join('Ranking The Stars Game uitnodiging van ' + user_name)
            first_link = '<a href="http://zapplive.ncrv.nl/rankingthestars">Ranking the Stars Game</a>'
            second_link = '<a href="http://zapplive.ncrv.nl">Z@PPLive</a>'
            message = join('Ik heb de ' + first_link + ' ontdekt en mijn score was ' + score + '. Game jij ook mee en help je punten te scoren voor de gezamenlijke ' + second_link + ' pot?')
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