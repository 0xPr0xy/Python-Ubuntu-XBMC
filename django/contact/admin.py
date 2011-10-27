from django.contrib import admin
from contact.models import Contact
from datetime import date
import xlwt
import tempfile
from django.http import HttpResponse

class ContactAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'subject', 'message',)
	actions = ['process_results']
    
	def process_results(self, request, queryset):
	   if queryset.count() < 1:
	       self.message_user(request, "Please select at least 1 row")
	       return 

	   contacts = Contact.objects.all()
	   filename = ('contact_data_dump_%s') % date.today()
	   wb = xlwt.Workbook()
	   ws = wb.add_sheet('A Test Sheet')
	   legend = ['Name', 'E-mail', 'Subject', 'Message', '',]
	   
	   c=0
	   for title in legend:
	       ws.write(0, c, title)
	       c += 1

	   r = 1
	   for contact in contacts:
	       row = [ contact.name, contact.email, contact.subject, contact.message, '']
	       for c in range(len(row)):
	           ws.write(r, c, row[c])
	       r+=1

	   f=tempfile.NamedTemporaryFile(delete=True)
	   wb.save(f.name)
	   response = HttpResponse(f.read(), mimetype='application/vnd.ms-excel')
	   f.close()
	   response['Content-Disposition'] = 'attachment; filename=%s.xls' % filename
	   return response

	process_results.short_description = "Export data"

admin.site.register(Contact, ContactAdmin)

