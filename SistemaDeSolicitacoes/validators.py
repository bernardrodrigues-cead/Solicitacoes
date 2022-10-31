from django.utils import timezone
from django.core.exceptions import ValidationError

def validate_is_future(date):
    if date <= timezone.now().date():
        raise ValidationError('A data prevista para gravação precisa ser no futuro.')

def validate_is_business_time(time):
    if time.hour < 8 or time.hour > 17:
        raise ValidationError('O horário de funcionamento do CEAD é de 8 às 18. Favor selecionar outro horário.')