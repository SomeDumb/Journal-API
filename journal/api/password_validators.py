import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class DigitsValidator:
    def validate(self, password, user=None):
        if not re.findall('[0-9]{1,}', password):
            raise ValidationError(
                ("The password must contain at least one digit"),
                code='digits',
            )
            
    def get_help_text(self):
            return _(
                "Your password must contain at least 1 digit."
            )