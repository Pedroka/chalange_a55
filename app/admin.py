from django.contrib import admin
from app.models import TicketCreditRequest

# Register your models here.

class TicketCreditRequestAdmin(admin.ModelAdmin):
    list_display = ('proposal_number','ticket_number','request_date', 'status')
    search_fields = ('proposal_number', 'ticket_number','name','cpf','status')

admin.site.register(TicketCreditRequest, TicketCreditRequestAdmin)
