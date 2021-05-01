"""
Define 
- application routes (= URLs)
- view functions (handlers for 1 or more routes): python functions executed
when a client request a given URL.
"""

# import 3rd-party modules
from flask import render_template, flash, redirect, url_for

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    View function to render login.html template with arguments `title` and `form`
    * Accepted methods: GET and POST requests
    - GET --> return info to client (e.g. web page)
    - POST --> submit form data to server 

    """
    # Create LoginForm instance
    form = LoginForm()

    # if data submitted by user is validated
    if form.validate_on_submit():
        # Create message to user
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        # redirect to index page
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)