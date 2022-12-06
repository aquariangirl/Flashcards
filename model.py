"""Models for flashcards app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.model):
     """User Class"""

    __tablename__ = "users"
    user_id = db.Column(db.Integer,
                        autoincrement= True
                        primary_key= True)
    username = db.Column(db.String VARCHAR(12), nullable= False, unique=True)
    password = db.Column(db.String VARCHAR(12), nullable= False, unique=True)
    email = db.Column(db.String, unique=True)
    phone = db.Column(db.String, unique=True)

    flashcards = db.relationship("flashcard", back_populates="user")

    def __repr__(self):
        """Display User info."""

        #think about what user information is needed in this return,
        #what would it be useful for?
        return f"<user_id = {self.user_id}, username = {self.username}, email = {self.email}>"



class Flashcard(db.model):
     """Flashcard Class"""

    __tablename__ = "flashcards"
    flashcard_id = db.Column(db.Integer,
                        autoincrement= True
                        primary_key= True)
    front_card = db.Column(db.Text, nullable= False)
    back_card = db.Column(db.Text, nullable= False)
    user_id = db.Column(db.Integer) #this needs to be the same as user.user_id
    category_id = db.Column(db.Integer
                        autoincrement= True)

    user = db.relationship("category", back_populates="flashcards")
    category = db.relationship("category", back_populates="flashcards")

    def __repr__(self):
        """Display Flashcard info."""

        return f"<flashcard_id = {self.user_id}, front_card = {self.front_card}, 
        back_card = {self.back_card}, category_id = {self.category_id}>"


class Category(db.model):
    """Category Class"""

    __tablename__ = "categories"
    category_id = db.Column(db.Integer,
                        autoincrement= True
                        primary_key= True)
    category_name = db.Column(db.String VARCHAR(50))

    flashcards = db.relationship("flashcard", back_populates="category")

def __repr__(self):
        """Display Category info."""

        return f"<category_id = {self.user_id}, category_name = {self.category_name}>"



def connect_to_db(flask_app, db_uri="postgresql:///ratings", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)


