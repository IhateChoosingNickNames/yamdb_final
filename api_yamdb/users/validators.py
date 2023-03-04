from rest_framework.exceptions import ValidationError


def additional_username_validator(value):
    """Дополнительная валидация для юзернейма."""
    if value == 'me':
        raise ValidationError('Такое имя пользователя недопустимо.')
