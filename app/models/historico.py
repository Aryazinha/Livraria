from datetime import datetime
from app import db


class Historico(db.Model):
    __tablename__ = 'historico'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', name="fk_historico_book_id"), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id', name="fk_historico_person_id"), nullable=False)
    borrow_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)