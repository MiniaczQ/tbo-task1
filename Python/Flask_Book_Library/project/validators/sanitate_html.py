from nh3 import clean
from typing import Optional


class UnsanitaryHtmlException(Exception):
    def __init__(self):
        super().__init__("Provided string contains unsanitary HTML")


def sanitate_html(value: Optional[str]):
    """
    If the string changed during sanitation, it contained a potentially unsanitary HTML.
    """
    if value is None:
        return
    if clean(value) != value:
        raise UnsanitaryHtmlException()
    return value
