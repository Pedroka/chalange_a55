from django.db import models
from .validade_fields import validate_credit

class TicketCreditRequest(models.Model):

    class Meta:
        db_table = 'ticket_credit_request'

    proposal_number = models.AutoField(primary_key=True)
    ticket_number = models.IntegerField(editable=False, null=True, blank=True)
    name = models.CharField(max_length=200)
    cpf = models.CharField(max_length=11)
    birth_date = models.DateField()
    request_date = models.DateField(auto_now_add=True, editable=False)
    credit_value = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_credit])
    status = models.CharField(default='Proposta em analise', max_length=25, editable=False)
    message_status = models.TextField(max_length=100, null=True, blank=True, editable=False)


    

