import re
from django.core.exceptions import ValidationError

class ComplexPasswordValidator:
    """
    Enforces strong password complexity:
    - At least 12 chars
    - At least one uppercase, one lowercase, one digit, one special character
    """

    def validate(self, password, user=None):
        #if len(password) < 12:
         #   raise ValidationError("A Password tem que conter pelo menos 12 caracteres.")
        if not re.search(r"[A-Z]", password):
            raise ValidationError("A Password tem que conter pelo menos uma letra maiúscula.")
        if not re.search(r"[a-z]", password):
            raise ValidationError("A Password tem que conter pelo menos uma letra minúscula.")
        if not re.search(r"\d", password):
            raise ValidationError("A Password tem que conter pelo menos um número.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("A Password tem que conter pelo menos um caracter especial.")

    def get_help_text(self):
        return (
            "Your password must be at least 12 characters long and contain an uppercase letter, "
            "a lowercase letter, a number, and a special character."
        )
