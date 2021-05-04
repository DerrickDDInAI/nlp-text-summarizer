"""
Python script to define child classes of FlaskForm 
"""
# import 3rd-party modules
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired


# Define classes
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

class TextForm(FlaskForm):
    """
    Class used by Flask-WTF extension to represent web forms
    Class variables: fields of the form with 
    - 1st argument: description or label
    - 2nd argument (optional): validators to assign validation behaviors to fields
    """
    # text = TextField('Insert a text', validators=[validators.required(), validators.Length(min=6, max=3000)])
    text_area = TextAreaField("TextArea", default="Please insert a text", validators=[DataRequired()]) # DataRequired to check that field is not submitted empty
    submit = SubmitField('Summarize!') # submit button


class UploadForm(FlaskForm):
    """
    Class used by Flask-WTF extension to represent web forms
    that deals with uploading files
    Class variables: fields of the form with 
    - 1st argument: description or label
    - 2nd argument (optional): validators to assign validation behaviors to fields
    """
    upload = FileField('text', validators=[
        FileRequired(),
        FileAllowed(['txt',], 'Text files only!')
    ])
    submit = SubmitField('Upload & Summarize!') # submit button