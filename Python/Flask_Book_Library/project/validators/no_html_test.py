from .no_html import NoHtml
from wtforms.i18n import DummyTranslations
from wtforms.validators import ValidationError, StopValidation
import pytest


# From https://github.com/wtforms/wtforms/blob/e22b0863023f44ddc96ff5b11d78dc26f52a012f/tests/conftest.py
class DummyField:
    _translations = DummyTranslations()

    def __init__(
        self,
        data=None,
        name=None,
        errors=(),
        raw_data=None,
        label=None,
        id=None,
        field_type="StringField",
    ):
        self.data = data
        self.name = name
        self.errors = list(errors)
        self.raw_data = raw_data
        self.label = label
        self.id = id if id else ""
        self.type = field_type

    def __call__(self, **other):
        return self.data

    def __str__(self):
        return self.data

    def __iter__(self):
        return iter(self.data)

    def _value(self):
        return self.data

    def iter_choices(self):
        return iter(self.data)

    def iter_groups(self):
        return []

    def has_groups(self):
        return False

    def gettext(self, string):
        return self._translations.gettext(string)

    def ngettext(self, singular, plural, n):
        return self._translations.ngettext(singular, plural, n)


@pytest.fixture
def dummy_field():
    return DummyField()


def test_valid_string(dummy_field):
    validator = NoHtml()
    dummy_field.data = "works"
    validator(None, dummy_field)


def test_none(dummy_field):
    validator = NoHtml()
    dummy_field.data = None
    validator(None, dummy_field)


def test_invalid_type(dummy_field):
    validator = NoHtml()
    dummy_field.data = 1
    with pytest.raises(ValidationError):
        validator(None, dummy_field)


def test_string_with_img(dummy_field):
    validator = NoHtml()
    dummy_field.data = '<img src="pic_trulli.jpg" alt="Italian Trulli">'
    validator(None, dummy_field)


def test_string__with_html_img_short(dummy_field):
    validator = NoHtml()
    dummy_field.data = '<img src="pic_trulli.jpg" alt="Italian Trulli"/>'
    with pytest.raises(StopValidation):
        validator(None, dummy_field)


def test_string_with_html_img_long(dummy_field):
    validator = NoHtml()
    dummy_field.data = '<img src="pic_trulli.jpg" alt="Italian Trulli"></img>'
    with pytest.raises(StopValidation):
        validator(None, dummy_field)


def test_string_with_script(dummy_field):
    validator = NoHtml()
    dummy_field.data = '<script>alert("Your compujter has been hacked")</script>'
    with pytest.raises(StopValidation):
        validator(None, dummy_field)
