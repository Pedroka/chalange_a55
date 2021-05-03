from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_credit(value):
    if value <= 0:
        raise ValidationError("Valor do Crédito menor ou igual a 0. Verifique!")