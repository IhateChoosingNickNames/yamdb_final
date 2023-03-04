import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def year_validator(value):
    if value > datetime.datetime.now().year:
        raise ValidationError(
            _("Задан некорректный год."),
            params={"value": value},
        )
