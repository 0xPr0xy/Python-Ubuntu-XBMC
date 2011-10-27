from django.db import models


class Contact(models.Model):
    name = models.CharField("Name", max_length=255,)
    email = models.EmailField()
    subject = models.CharField("Subject", max_length=255,)
    message = models.TextField("Message", max_length=1000,)
    subscribe = models.BooleanField("Yes, I'd like to receive the newsletter.", blank=True)
   
    
   
