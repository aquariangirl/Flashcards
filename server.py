"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined



@app.route('/')
def homepage():

    return render_template('homepage.html')

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    phone = request.form.get("phone")

    user = crud.get_user_by_username(username)

    if user:
        flash("Cannot create an account with that username. Try again.")
    else:
        user = crud.create_user(username, password, email, phone)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")
    # TODO add else statements if password is missing
    # TODO remember to add function to update email and phone if user chooses to add later


@app.route("/login", methods=["POST"])
def login_user():
    """Login user."""

    username = request.form.get("username")
    password = request.form.get("password")

    user = crud.get_user_by_username(username)

    if user:
        if user.password == password:
            session['user_id'] = user.user_id
            print(f"{user.username}'s test: user _ id = {session['user_id']}") #TODO the underscore is for sample data only?
            flash("Logged In!")
        else:
            flash("Incorrect password! Try again.")
    else:
        flash("No account associated with email.")

    return redirect("/user-profile")


@app.route('/user-profile')
def show_my_profile():
    """Shows the users own profile."""

    if "user_id" in session:
        user = crud.get_user_by_id(session["user_id"])
        return render_template('user-profile.html', user=user)

    else:
        flash("Please log in to view your profile.")
        return redirect("/")


@app.route('/categories')
def all_categories():

    categories = crud.get_all_categories()

    return render_template('categories.html', categories=categories)


@app.route('/categories/<flashcard_id>')
def show_flashcard(flashcard):

    flashcard = crud.get_flashcard_by_category(flashacrd_id)

    return render_template('movie_details.html', movie=movie)





@app.route('/find-user') # TODO
def find_user(flashcard):


    return render_template('find-user.html') #, movie=movie)



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)