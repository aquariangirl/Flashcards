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


@app.route('/categories/<flashcard_id>') # TODO
def show_flashcard(flashcard):

    flashcard = crud.get_flashcard_by_category(flashcard_id)

    return render_template('flashcards.html') #, flashcard=flashcard)



@app.route('/create-flashcard', methods=['POST'])
def create_flashcard():

    if session.get('user_id'):
        front = request.form.get('front_card')
        back = request.form.get('back_card')
        category = request.form.get('category_name')
        user = session['user_id']
        print(user)
        print(front)
        print(back)
        category_id = crud.get_category_id(category)


    flashcard = crud.create_flashcard(front_card=front, back_card=back, category_id=category_id, user_id=user)
    db.session.add(flashcard)
    db.session.commit()
    
    return render_template("all-flashcards.html")


@app.route('/new-flashcard') # TODO
def new_flashcard():
    """Shows selected Category -- and allows user to input new flashcard data""" 
    
    category = request.args.get("category-choice")
    print("*"*20)
    print(category)

    return render_template('new-flashcard.html', category_choice=category) #, category_id=category_id)
    



#have user add a category, then add a flashcard which can be added to the category
# @app.route('/new-flashcard/<category_id>') #, methods=['POST']) # TODO
# def add_new_flashcard(category_id):
#     """Shows where logged-in user inputs flashcard data""" 
    
#     #statement that will show the selected category
#     category = request.args.get("category-choice")


#     # #
#     # category = category_id

#     # if session.get('user_id'):
#     #     front = request.form.get('front_card')
#     #     back = request.form.get('back_card')
#     #     user = session['user_id']
#     #     print(user)

#     #     flashcard = crud.create_flashcard(front, back, category_id=category, user_id=user)
#     #     db.session.add(flashcard)
#     #     db.session.commit()
#     #     flashcard_id = flashcard.flashcard_id

#         return render_template('/all-flashcards.html')
#         # return redirect(f'/flashcards/{flashcard_id}')

#     else:
#         flash("Please log in to create a flashcard.")

#         # #

        #return redirect(f'/flashcards/{flashcard_id}') #uncomment once done playing with flashcard hardcode


@app.route("/select-category") #TODO
def select_past_category():
    """Selects a previously added category"""

    #statment that gets category name from database ?
    category_names = crud.get_all_categories()

    #  category = category_id

    # if session.get('user_id'):
    #     my_category = request.form.get('category_name')
    #     user = session['user_id']
    #     # print(user)

    #     category = crud.create_category(category_name=my_category)
    #     db.session.add(category)
    #     db.session.commit()
    #     category_id = category.category_id

    return render_template('select-category.html', categories=category_names)


    return redirect("/new-flashcard") #, categories=category_names) #after POST, redirect to ("/new-flashcard")


@app.route('/find-user') # TODO
def find_user(flashcard):


    return render_template('find-user.html') #, movie=movie)



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)