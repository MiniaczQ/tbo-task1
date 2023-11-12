import pytest
from .sanitate_html import sanitate_html, UnsanitaryHtmlException


def test_valid_string():
    sanitate_html("works")


def test_none():
    sanitate_html(None)


def test_img_tag_without_trailing_slash():
    sanitate_html('<img src="pic_trulli.jpg" alt="Italian Trulli">')


def test_img_tag_with_trailing_slash():
    # HTML-wise same as above, the `/` gets removed and causes false positive, better safe than sorry
    with pytest.raises(UnsanitaryHtmlException):
        sanitate_html('<img src="pic_trulli.jpg" alt="Italian Trulli"/>')


def test_img_tag_with_content():
    with pytest.raises(UnsanitaryHtmlException):
        sanitate_html('<img src="pic_trulli.jpg" alt="Italian Trulli"></img>')


def test_script_tag():
    with pytest.raises(UnsanitaryHtmlException):
        sanitate_html('<script>alert("Your compjuter has been hacked")</script>')
