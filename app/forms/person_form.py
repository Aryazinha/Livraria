from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email

class PersonForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired(), Length(min=2, max=20)])
    sobrenome = StringField('Sobrenome', validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Login')