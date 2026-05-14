from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo


class BookForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    author = StringField('Autor', validators=[DataRequired()])
    genero = StringField('Gênero', validators=[DataRequired()])
    available = BooleanField('Disponível')
    submit = SubmitField('Adicionar Livro')