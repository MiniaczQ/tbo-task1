from project import db, app
from ..validators.sanitate_html import sanitate_html
from typing import Optional


# Book model
class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    author = db.Column(db.String(64))
    year_published = db.Column(db.Integer)
    book_type = db.Column(db.String(20))
    status = db.Column(db.String(20), default="available")

    def __init__(
        self,
        name: str,
        author: str,
        year_published: int,
        book_type: str,
        status: str = "available",
    ):
        self.name = sanitate_html(name)
        self.author = sanitate_html(author)
        self.year_published = year_published
        self.book_type = sanitate_html(book_type)
        self.status = sanitate_html(status)

    def update(
        self,
        name: Optional[str],
        author: Optional[str],
        year_published: Optional[int],
        book_type: Optional[str],
    ):
        if name is not None:
            self.name = sanitate_html(name)
        if author is not None:
            self.author = sanitate_html(author)
        if year_published is not None:
            self.year_published = year_published
        if book_type is not None:
            self.book_type = sanitate_html(book_type)

    def __repr__(self):
        return f"Book(ID: {self.id}, Name: {self.name}, Author: {self.author}, Year Published: {self.year_published}, Type: {self.book_type}, Status: {self.status})"


with app.app_context():
    db.create_all()
