from django.test import TestCase
from app.models import TicketCreditRequest
from app.serializer import TicketCreditRequestSerializer


class TestTicket(TestCase):

    def setUp(self):
        data_test = {
            "name": "teste name",
            "cpf": "22222222222",
            "birth_date": "1990-01-01",
            "credit_value": 40000.00
        }

        serializer = TicketCreditRequestSerializer(data=data_test)

        if serializer.is_valid():
            serializer.save()

        self.proposal_number = serializer.data['proposal_number']

    def test_object_created(self):
        self.assertEqual(TciketCreditRequest.objects.count(),1)

    def test_search_ticket(self):
        ticket_found = TciketCreditRequest.objects.get(proposal_number=self.proposal_number)
