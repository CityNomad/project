from django.core.exceptions import ValidationError


def validate_title(value):
    if len(value) > 20:
        raise ValidationError("Название должно быть короче 20 символов")
    if len(value) < 4:
        raise ValidationError("Название должно быть не короче 4 символов")
    return value


def validate_description(value):
    if len(value) > 1000:
        raise ValidationError("Максимальное количество - 1000 символов")
    return value
