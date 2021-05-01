"""
Define 
- application routes (= URLs)
- view functions (handlers for 1 or more routes): python functions executed
when a client request a given URL.
"""

# import 3rd-party modules
from flask import render_template

# import local modules
from app import app # from app package import app (instance of Flask object)
from app.forms import LoginForm

# Define routes and view functions
## decorators to associate URLs "/" and "/index" to the function
@app.route("/")
@app.route('/index')
def index():
    """
    View function to render index.html template
    with arguments: 
        - title
        - user
        - posts
    """
    user = {'username': 'Todo'}
    posts = [
        {
            'author': {'username': 'Sangoku'},
            'body': 'I like to fight!'
        },
        {
            'author': {'username': 'Chichi'},
            'body': 'Do your homework, Sangoten!'
        }
    ]
    # return render_template('index.html', title="Home", user=user)
    return render_template('index.html', user=user, posts=posts)


@app.route('/login')
def login():
    """
    View function to render login.html template
    with arguments: 
        - title
        - form
    """
    # Create LoginForm instance
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)