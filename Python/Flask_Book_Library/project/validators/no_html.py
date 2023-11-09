from wtforms.validators import ValidationError, StopValidation
from nh3 import clean


class NoHtml:
    """
    Checks if a string is clean of any HTML shenanigans
    """

    def __init__(self, message=None):
        self.message = message
        self.field_flags = {"no_html": True}

    def __call__(self, form, field):
        if field.data is None:
            return

        if not isinstance(field.data, str):
            raise ValidationError(f"Type is not {str.__name__}")

        if clean(field.data) != field.data:
            raise StopValidation(self.message or "Field contains HTML")
