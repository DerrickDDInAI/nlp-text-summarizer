"""
`__init__.py` file to consider the sub-directory `app` as a package
=> can be imported. 
When imported, `__init__.py` is executed.
"""
# import 3rd-party modules
from flask import Flask
from flask_bootstrap import Bootstrap

# import local modules
from .config import Config

# instantiate Flask object with name of module
app = Flask(__name__)

# method to make Flask object read and apply Config object
app.config.from_object(Config)

# initalize Flask-Bootstrap
bootstrap = Bootstrap(app)

# import routes at the bottom to avoid error from circular imports
from app import routes
