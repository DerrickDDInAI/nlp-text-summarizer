"""
Define 
- application routes (= URLs)
- view functions (handlers for 1 or more routes): python functions executed
when a client request a given URL.
"""

# import local modules
from app import app # from app package import app (instance of Flask object)

# Define routes and view functions
## decorators to associate URLs "/" and "/index" to the function
@app.route("/")
@app.route('/index')
def index():
    """
    View function to return a string
    """
    return "Test"