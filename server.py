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


@app.route("/logout") 
def logout_user():
    """Logout user."""

    session.pop('user_id', None)
    flash("You have been logged out.")

    return redirect("/")


@app.route('/user-profile')
def show_my_profile():
    """Shows the users own profile."""

    if "user_id" in session:
        user = crud.get_user_by_id(session["user_id"])
        return render_template('user-profile.html', user=user)

    else:
        flash("Please log in to view your profile.")
        return redirect("/")


@app.route('/update-user-profile')
def update_contacts():
    """Allows user to update contact info."""

    if session.get('user_id'):
        id = session['user_id']
        current_user = crud.get_user_by_id(id)
        print(current_user.phone)
        print(current_user.email)

    return render_template('update-contact.html', phone=current_user.phone, email=current_user.email)

@app.route('/update-information', methods=['POST'])
def update_information():

    if session.get('user_id'):
        phone = request.form.get('phone')
        email = request.form.get('email')
        user = session['user_id']
        print(phone)
        print(email)
        print(user)

    current_user = crud.get_user_by_id(user)
    current_user.phone = phone
    current_user.email = email

    db.session.commit()

    return "Updated"

@app.route('/categories')
def all_categories():

    categories = crud.get_all_categories()

    return render_template('categories.html', categories=categories)


@app.route('/my-flashcards')
def show_my_flashcards():
    """Displays all flashcards created by user"""

    user_id = session['user_id']

    my_flashcards = crud.get_flashcards_by_user(user_id)

    return render_template('my-flashcards.html', flashcards=my_flashcards, user_id=user_id)


@app.route("/select-category")
def select_past_category():
    """Selects a previously added category"""

    category_names = crud.get_all_categories()

    
    return render_template('select-category.html', categories=category_names)


@app.route('/create-category', methods=['POST'])
def create_category():
    """Add a new category to database"""

    if session.get('user_id'):
        my_category = request.form.get('new-category')
        user = session['user_id']
        # print(user)
        
    category = crud.create_category(category_name=my_category)
    db.session.add(category)
    db.session.commit()

    category_id = crud.get_category_id(my_category)
    print(category_id)

    return render_template('new-flashcard.html', category_choice=my_category)


@app.route('/categories/<category_name>')
def show_category_flashcards(category_name):
    """Displays all flashcards within a single category."""

    category = crud.get_category_name(category_name)

    flashcards = crud.get_flashcards_by_category(category_name) # edit to get all flashcards by catergory ?
    # print("*"*20)
    for flashcard in flashcards:
        print(flashcard)

    return render_template('flashcards-in-category.html', category_name=category, flashcards=flashcards)


@app.route('/categories/<category_name>/<flashcard_id>')
def show_flashcard(category_name, flashcard_id):
    """Displays a single flashcard"""

    #there needs to be instructions on where to get the category_name and flashcard_id
    # category_name = crud.get_category_id(category_name)
    # flashcard = crud.get_flashcard_by_id(flashcard_id)

    flashcards = crud.get_all_flashcards() #this works
    flashcard = crud.get_flashcard_by_id(flashcard_id) #this works
    # print(flashcards)

    return render_template('view-flashcard.html', flashcard=flashcard)


@app.route('/create-flashcard', methods=['POST'])
def create_flashcard():
    """Creates a flashcard"""

    if session.get('user_id'):
        front = request.form.get('front_card')
        back = request.form.get('back_card')
        category = request.form.get('category_name')
        user = session['user_id']
        # print(user)
        # print(front)
        # print(back)
        # print(category)
        category_id = crud.get_category_id(category) 
        # print(category_id)


    flashcard = crud.create_flashcard(front_card=front, back_card=back, category_id=category_id, user_id=user)
    db.session.add(flashcard)
    db.session.commit()
    
    return redirect(f'/categories/{category}/{flashcard.flashcard_id}')


@app.route('/delete-flashcard')
def delete_flashcard():
    """Deletes a flashcard"""

#get flashcard by id to delete the flashcard

    db.session.delete(flashcard)
    db.session.commit() 

    return render_template('delete-flashcard.html')



@app.route('/new-flashcard')
def new_flashcard():
    """Shows selected Category -- and allows user to input new flashcard data""" 
    
    category = request.args.get("category-choice")
    # print("*"*20)
    # print(category)

    return render_template('new-flashcard.html', category_choice=category) #, category_id=category_id)
    

    return redirect("/new-flashcard") #, categories=category_names) #after POST, redirect to ("/new-flashcard")


@app.route("/search")
def search():
    return render_template("search.html")


@app.route("/flashcardresult", methods=['POST'])
def flashcard_result():
    keyword = request.form.get("keyword")
    # list1 = []
     
    results = crud.search_flashcards(keyword) # create crud function that will is LIKE % to return keyword searched
    # for i in results:
        # if ( keyword in i.keyword) is True:
        #     list1.append(i.keyword)
    print("*"*20)
    print(results)


    return render_template("flashcardresult.html", results=results)
    # session.commit()



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)