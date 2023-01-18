"""Models for flashcards app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User Class"""

    __tablename__ = "users"
    user_id = db.Column(db.Integer, autoincrement= True, primary_key= True)
    username = db.Column(db.String(15), nullable= False, unique=True)
    password = db.Column(db.String(25), nullable= False)
    email = db.Column(db.String(25), unique=True)
    phone = db.Column(db.String(20), unique=True)

    flashcards = db.relationship("Flashcard", back_populates="user")
    # categories = db.relationship("Category", back_populates="user")

    def __repr__(self):
        """Display User info."""

        #think about what user information is needed in this return string,
        #what would it be useful for?
        return f"<user_id = {self.user_id}, username = {self.username}>"



class Flashcard(db.Model):
    """Flashcard Class"""

    __tablename__ = "flashcards"
    flashcard_id = db.Column(db.Integer, autoincrement= True, primary_key= True)
    front_card = db.Column(db.Text, nullable= False)
    back_card = db.Column(db.Text, nullable= False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    user = db.relationship("User", back_populates="flashcards")
    category = db.relationship("Category", back_populates="flashcards")

    def __repr__(self):
        """Display Flashcard info."""

        return f"<flashcard_id = {self.flashcard_id}, front_card = {self.front_card}, category_id = {self.category_id}>"


class Category(db.Model):
    """Category Class"""

    __tablename__ = "categories"
    category_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True)
    category_name = db.Column(db.String(50))
    # user_id = db.Column(db.Integer, 
    #                     db.ForeignKey("users.user_id"))

    flashcards = db.relationship("Flashcard", back_populates="category")
    # user = db.relationship("User", back_populates="categories")

    def __repr__(self):
        """Display Category info."""

        return f"<category_id = {self.user_id}, category_name = {self.category_name}>"



def connect_to_db(flask_app, db_uri="postgresql:///flashcards", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)


