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

    # Specify port as some services only open specific ports
    port = int(os.environ.get('PORT', 5000))