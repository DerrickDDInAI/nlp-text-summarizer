"""

"""

# import 3rd-party modules
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

# Define class
class LoginForm(FlaskForm):
    """
    Class used by Flask-WTF extension to represent web forms
    Class variables: fields of the form with 
    - 1st argument: description or label
    - 2nd argument (optional): validators to assign validation behaviors to fields
    """
    username = StringField('Username', validators=[DataRequired()]) # DataRequired to check that field is not submitted empty
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me') # check box
    submit = SubmitField('Sign In') # submit button