from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class ExtensionForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    extension = StringField('Ramal', validators=[DataRequired()])
    password = StringField('Senha', validators=[DataRequired()])
