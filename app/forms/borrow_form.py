from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class BorrowForm(FlaskForm):
    book_id = SelectField('Livro', coerce=int, validators=[DataRequired()])
    person_id = SelectField('Pessoa', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Registrar Empréstimo')