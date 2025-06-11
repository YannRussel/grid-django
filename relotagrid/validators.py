from django.core.exceptions import ValidationError

def validate_numero_congo(value):
    if not (value.startswith('05') or value.startswith('06') or value.startswith('04')):
        raise ValidationError('Le numéro doit commencer par 05, 06 ou 04.')