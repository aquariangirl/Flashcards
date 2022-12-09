"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


#routes and view functions:
@app.route('/')
def homepage():

    return render_template('homepage.html')


@app.route('/categories')
def all_categories():

    categories = crud.get_all_categories()

    return render_template('categories.html', categories=categories)


@app.route('/categories/<flashcard_id>')
def show_flashcard(flashcard):

    flashcard = crud.get_flashcard_by_category(flashacrd_id)

    return render_template('movie_details.html', movie=movie)





if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)