import pytest
from .models import Book
from ..validators.sanitate_html import UnsanitaryHtmlException


def test_create_success():
    Book("a", "b", 0, "c", "d")


@pytest.mark.parametrize(
    "name,author,book_type,status",
    [
        ("<script>alert(0)</script>", "b", "c", "d"),
        ("a", "<script>alert(0)</script>", "c", "d"),
        ("a", "b", "<script>alert(0)</script>", "d"),
        ("a", "b", "c", "<script>alert(0)</script>"),
    ],
)
def test_create_with_unsanitary_html(name, author, book_type, status):
    with pytest.raises(UnsanitaryHtmlException):
        Book(name, author, 0, book_type, status)


@pytest.fixture
def book():
    return Book("a", "b", 0, "c", "d")


def test_edit_success(book):
    book.update("a", "b", 0, "c")


@pytest.mark.parametrize(
    "name,author,book_type",
    [
        ("<script>alert(0)</script>", "b", "c"),
        ("a", "<script>alert(0)</script>", "c"),
        ("a", "b", "<script>alert(0)</script>"),
    ],
)
def test_edit_with_unsanitary_html(book, name, author, book_type):
    with pytest.raises(UnsanitaryHtmlException):
        book.update(name, author, 0, book_type)
