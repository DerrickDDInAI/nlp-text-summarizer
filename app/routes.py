"""
Define 
- application routes (= URLs)
- view functions (handlers for 1 or more routes): python functions executed
when a client request a given URL.
"""
# =====================================================================
# Import
# =====================================================================

# import internal modules
import os.path

# import 3rd-party modules
from flask import render_template, flash, redirect, url_for, request, send_from_directory, abort
from werkzeug.utils import secure_filename
from transformers import pipeline

# import local modules
from app import app # from app package import app (instance of Flask object)
from app.forms import LoginForm, TextForm, UploadForm


# load pre-trained summarization pipeline
global summarizer
summarizer = pipeline("summarization")

# =====================================================================
# Functions
# =====================================================================

def allowed_file(filename):
    """
    Function to check whether the file to be uploaded
    has an allowed extension
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

def summarize(text, summarizer, min_length=30, max_length=130):
    """
    Function to summarize a text
    """
    # summarize text
    summary = summarizer(text, min_length=min_length, max_length=max_length, do_sample=False)

    return summary[0]["summary_text"]

# =====================================================================
# Routes and view functions
# =====================================================================

# decorators to associate URLs "/" and "/text" to the function
@app.route("/", methods=['GET', 'POST'])
@app.route('/text', methods=['GET', 'POST'])
def text():
    """
    View function to render text.html template with arguments `title` and `form`
    * Accepted methods: GET and POST requests
    - GET --> return info to client (e.g. web page)
    - POST --> submit form data to server 

    """
    # Create LoginForm instance
    form = TextForm()

    # if data submitted by user is validated
    if form.validate_on_submit():
        # Create message to user
        flash(f'Text requested to summarize')
        # summarize
        summary = summarize(form.text_area.data, summarizer)
        return render_template('text.html', title='Summarize a text', form=form, summary=summary)
    
    return render_template('text.html', title='Summarize a text', form=form)


@app.route('/book', methods=['GET', 'POST'])
def book():
    """
    View function to render book.html template with arguments `title` and `form`
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

    return render_template('book.html', title='Sign In', form=form)


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    """
    View function to render upload_file.html template with arguments `title` and `form`
    * Accepted methods: GET and POST requests
    - GET --> return info to client (e.g. web page)
    - POST --> submit form data to server 

    """
    # if request.method == 'POST':
    #     # check if the post request has the file part
    #     if 'file' not in request.files:
    #         flash('No file part')
    #         return redirect(request.url)
    #     file = request.files['file']
    #     # if user does not select file, browser also
    #     # submit an empty part without filename
    #     if file.filename == '':
    #         flash('No selected file')
    #         return redirect(request.url)
    #     if file and allowed_file(file.filename):
    #         filename = secure_filename(file.filename)
    #         # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Create UploadForm instance
    form = UploadForm()
    
    if form.validate_on_submit():
        file = form.upload.data
        # filename = secure_filename(file.filename)
        # f.save(os.path.join(
        #     app.instance_path, 'photos', filename
        # ))
        # return redirect(url_for('index'))
        file.seek(0)
        text = file.read().decode("utf-8")
        print(type(text))

        # Create message to user
        flash(f'Text requested to summarize')
        
        # summarize
        summary = summarize(text, summarizer)

        # # Create LoginForm instance
        # form = TextForm()
        
        # # if data submitted by user is validated
        # if form.validate_on_submit():
        #     # create message to user
        #     flash(f'Text requested to summarize')
            
        #     # summarize
        #     summary = summarize(text)
        #     return render_template('upload_file.html', title='Summarize a text', form=form, summary=summary)

        # return redirect(url_for('uploaded_file',
        #                         filename=filename))
        return render_template('upload_file.html', title='Upload a File', form=form, summary=summary)
    return render_template('upload_file.html', title='Upload a File', form=form)

@app.route('/upload/<filename>')
def uploaded_file(filename):
    """
    View function to return file
    * param: filename of the uploaded file from upload_file()
    """
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename=filename)
    except FileNotFoundError:
        abort(404)
