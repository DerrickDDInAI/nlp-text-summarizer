"""
Python script to define child classes of FlaskForm 
"""
# =====================================================================
# Import
# =====================================================================

# import 3rd-party modules
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired

# import local modules
from app.static.data.default_text import default_text, source

# Define classes
class SearchForm(FlaskForm):
    """
    Class used by Flask-WTF extension to represent web forms
    Class variables: fields of the form with 
    - 1st argument: description or label
    - 2nd argument (optional): validators to assign validation behaviors to fields
    """
    search = StringField('Search Books')
    # check_box = BooleanField('Remember Me') # check box
    submit = SubmitField('Search!') # submit button

class TextForm(FlaskForm):
    """
    Class used by Flask-WTF extension to represent web forms
    Class variables: fields of the form with 
    - 1st argument: description or label
    - 2nd argument (optional): validators to assign validation behaviors to fields
    """
    source = source
    # text = TextField('Insert a text', validators=[validators.required(), validators.Length(min=6, max=3000)])
    text_area = TextAreaField("TextArea", default=default_text, validators=[DataRequired()]) # DataRequired to check that field is not submitted empty
    min_input = IntegerField('Min summary length', default=30)
    max_input = IntegerField('Max summary length', default=130)
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
    min_input = IntegerField('Min summary length', default=30)
    max_input = IntegerField('Max summary length', default=130)
    submit = SubmitField('Upload & Summarize!') # submit button