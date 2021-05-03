from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import generics
from .serializer import TicketCreditRequestSerializer
import requests
from .models import TicketCreditRequest
from .tasks import validate_credit
from datetime import date
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.DEBUG)


@api_view(['POST'])
def create_ticket(request):
    
    ###LOG INFO###
    logger.info("Chamada do endpoint feita com sucesso!!")
    logger.info(f"Dados: {request.data}")

    serializer = TicketCreditRequestSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        #Ticket number generate
        ticket_number = str(date.today().year)+str(date.today().month)+str(serializer.data['proposal_number'])
        TicketCreditRequest.objects.filter(proposal_number=serializer.data['proposal_number']).update(ticket_number=ticket_number)
               
        json_response = {
            "proposal_number":serializer.data['proposal_number'],
            "ticket_number": ticket_number,
            "name": serializer.data["name"],
            "request_date": serializer.data["request_date"],
            "status": serializer.data["status"]
            }
        logger.info(f"Ticket gerado com sucesso: {ticket_number}")

        validate_credit.apply_async(countdown=60,expires=120)
        logger.info("Enviado para fila assincrona de validacao...")

        return Response(json_response, status=status.HTTP_201_CREATED)
    
    logger.info(f"Error: {serializer.errors.get(list(serializer.errors.keys())[0])[0]}")

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def search_ticket(request):
    
    try:
        logger.info(f"Procurando ticket {request.data['ticket_number']}")
        ticket = TicketCreditRequest.objects.get(ticket_number=request.data["ticket_number"])
    except:
        logger.info(f"Ticket {request.data['ticket_number']} nao encontrado")
        return Response({"message_error":"Ticket não encontrado"},status=status.HTTP_404_NOT_FOUND)
    
    json_response = {
        "proposal_number": ticket.proposal_number,
        "name": ticket.name,
        "request_date":ticket.request_date,
        "status":ticket.status,
        "message_status": ticket.message_status
    }

    return Response(json_response, status=status.HTTP_200_OK)


