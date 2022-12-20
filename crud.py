"""CRUD Operations"""

from model import db, User, Category, Flashcard, connect_to_db

def create_user(username, password, email, phone):
    """Create and return a new user."""

    user = User(username=username, password=password, email=email, phone=phone)

    return user


def get_user_by_username(username):
    """Gets a user by their username""" #so they can login with username

    user = User.query.filter(User.username== username).first()

    return user


def get_user_by_id(user_id):
    """Gets a user by their id"""

    user = User.query.filter(User.user_id== user_id).first()

    return user

# TODO create function that allows user to create a category
#when user creates a flashcard, they much select which category to add the flashcard to

# def create_category(category_id):
#     """Allows user to create a category"""

#     category = Category(category_name)

#     return category


def create_category(category_name):
    """Create category"""

    category = Category(category_name=category_name)

    return category


def create_flashcard(front_card, back_card, category_id, user_id):
    """Create and return a new flashcard"""

    flashcard = Flashcard(front_card=front_card, back_card=back_card, category_id=category_id, user_id=user_id)

    return flashcard





def get_all_users():
    """Get a list of all users"""

    all_users = db.session.query(User.user_id, User.username).all()

    return all_users
    

# def show_my_profile(): # TODO
#     """Get a users profile"""

#     my_profile = db.session.get(User.user_id, User.username)

#     return my_profile


def get_all_flashcards():
    """Get a list of all flashcards"""

    all_flashcards = db.session.query(Flashcard.flashcard_id).all()

    return all_flashcards


def get_all_categories():
    """Get a list of all categories"""

    all_categories = db.session.query(Category.category_id, Category.category_name).all()

    return all_categories


def get_category_id(category_name): # TODO
    """Get category id by its name"""
    
    categories = Category.query.filter(Category.category_name==category_name).first()
    
    if categories:
        return categories.category_id


def get_flashcard_by_category(category_name):
    """Get a flashcard by its category"""

    flashcard = Flashcard.query.get(category_name)

    return flashcard


def get_category_name(category_id):
    """Get a flashcard by its category name"""

    # flashcard = Flashcard.query.get(category_name)
    category = Category.query.get(category_id)
    category_name = category.category_name

    return category_name


def get_flashcard_by_user():
    """Get a flashcard by its user"""

    flashcard = Flashcard.query.get(User.user_id)

    return flashcard


def get_user_by_flashcard():
    """Get a user by their flashcard"""

    user = User.query.get(Flashcard.flashcard_id)

    return user



if __name__ == '__main__':
    from server import app
    connect_to_db(app)







