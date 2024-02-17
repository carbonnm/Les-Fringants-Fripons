from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms import SubmitField
from wtforms import PasswordField

from wtforms.validators import InputRequired
from wtforms.validators import Length
from wtforms.validators import EqualTo
from wtforms.validators import ValidationError
from wtforms.validators import DataRequired

class LoginForm(FlaskForm) :
    """
    Login Form 
    --------------
    Formulary that needs to be submitted when the user wants to login.
    """
    username = StringField('Pseudo', validators = [InputRequired(message = "Entrez votre pseudo")])
    password = PasswordField('Mot de passe', validators = [InputRequired(message = "Entrez votre mot de passe")])

    submit = SubmitField('Se connecter')