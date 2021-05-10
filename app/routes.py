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
from os import link
import os.path

# import 3rd-party modules
from flask import render_template, flash, redirect, url_for, request, send_from_directory, abort
from werkzeug.utils import secure_filename
from transformers import pipeline
import pandas as pd

# import local modules
from app import app # from app package import app (instance of Flask object)
from app.forms import SearchForm, TextForm, UploadForm
from app.scrape import search_books, get_book_text
from app.summarizer import gensim_summary


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

        # Get min_length and max_length
        min_length = form.min_input.data or 30
        max_length = form.max_input.data or 130

        # summarize
        summary = summarize(form.text_area.data, summarizer, min_length, max_length)
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
    search_form = SearchForm()

    # if data submitted by user is validated
    if search_form.validate_on_submit():

        # create message to user
        flash(f'Search requested for user')

        # search results
        search_results: pd.DataFrame = search_books(search_form.search.data)

        # create lambda function to make book_id clickable
        # link_frmt = lambda x: '''<a href="#" target="popup" 
        #               onclick="window.open('summarize_book/{0}', 
        #               'name','width=600,height=400')">{0}</a>'''.format(x)

        ## target "_blank" to open link in a new tab/window depending on browser's settings
        link_frmt = lambda x: f'<a href="summarize_book/{x}" target="_blank">{x}</a>' 

        return render_template(
            'book.html',
            title = "Summarize a book",
            form=search_form,
            tables=[search_results.to_html(
                # formatters={'book_id':lambda x:f'<a href="{{{{ url_for(\'summarize_book\', book_id={x}) | safe }}}}">{x}</a>'},
                formatters={"book_id": link_frmt},
                justify='center', 
                classes='search_results', 
                render_links=True,
                escape=False)],
            # titles=search_results.columns.values
            titles=['search']
            )
        
    return render_template('book.html', title="Summarize a book", form=search_form)
      # return render_template('dataframe.html',tables=[sr.to_html(justify='center, classes='table table-bordered table-hover')],titles = [filename], form=form) 

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    """
    View function to render upload_file.html template with arguments `title` and `form`
    * Accepted methods: GET and POST requests
    - GET --> return info to client (e.g. web page)
    - POST --> submit form data to server 

    """
    # Create UploadForm instance
    form = UploadForm()
    
    # if data submitted by user is validated 
    if form.validate_on_submit():
        file = form.upload.data
        filename = secure_filename(file.filename)
        # f.save(os.path.join(
        #     app.instance_path, 'photos', filename
        # ))
        # return redirect(url_for('index'))
        file.seek(0)
        text = file.read().decode("utf-8")

        # Create message to user
        flash(f'Text requested to summarize')

        # Get min_length and max_length
        min_length = form.min_input.data or 30
        max_length = form.max_input.data or 130        
        
        # summarize
        summary = summarize(text, summarizer, min_length, max_length)

        return render_template('upload_file.html', title='Upload a File', form=form, filename=filename, summary=summary)
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

@app.route('/summarize_book/<book_id>')
def summarize_book(book_id):
    """
    View function to return file
    * param: book
    """
    # ebook link
    link = "https://www.gutenberg.org/ebooks/" + book_id
    
    # get book text
    book_text = get_book_text(link)

    # sample from book
    sample = book_text[:1000]

    # Extractive summary
    extractive_summary = gensim_summary(book_text)



    return render_template('book_summary.html', title='Book Summary', book_id=book_id, sample=sample, extractive_summary=extractive_summary)
