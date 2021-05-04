# import internal modules
import os

# Define Config class
class Config(object):
    """
    Config class to store config variables:
    - SECRET_KEY: cryptographic key to generate signatures or tokens;
    used by Flask-WTF extension to protect web forms against Cross-Site Request Forgery (CSRF).
    """
    # secret key with defaut value if no environment variable `SECRET_KEY` returns None
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key-hard-to-guess'

    # specify port as some services only open specific ports
    port = int(os.environ.get('PORT', 5000))

    # absolute path where to store uploaded files
    UPLOAD_FOLDER = os.path.abspath('app/static/client/')
    # UPLOAD_FOLDER = /Users/derrickvanfrausum/BeCode_AI/git-repos/nlp-text-summarizer/app/static/client
    
    # set of allowed file  extensions
    ALLOWED_EXTENSIONS = {'txt', 'pdf'}
    # ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}