from __future__ import absolute_import
from celery import shared_task
from celery.decorators import task
from .models import TicketCreditRequest
from datetime import date
from dateutil.relativedelta import relativedelta

@task(
    name="validate_credit_request",
    
    max_retries=5,
    soft_time_limit=20)
def validate_credit():
    
    ticket = TciketCreditRequest.objects.filter(status='Proposta em analise')
    today = date.today()
    propostas = []

    for i in ticket:
        if relativedelta(today, i.birth_date).years <= 18 or i.credit_value > 100000.00:
            i.status = 'Proposta Recusada'
            i.message_status = 'O Solicitante deve ter mais de 18 anos e o Valor do Crédito abaixo de R$ 100.000,00'
            propostas.append(i.proposal_number)
            i.save()
        else:
            i.status = 'Proposta Aprovada'
            i.message_status = 'Em breve entraremos em contato para liberação do Crédito.'
            propostas.append(i.proposal_number)
            i.save()

    return f'Propostas {propostas} validadas com sucesso!!!'