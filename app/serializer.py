from rest_framework import serializers
from .models import TicketCreditRequest

class TicketCreditRequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TicketCreditRequest
        fields = '__all__'