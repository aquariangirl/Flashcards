"""Script to create and populate database"""

import os
import json
from random import choice

import crud
import model
import server

os.system("dropdb flashcards")
os.system("createdb flashcards")
model.connect_to_db(server.app)
model.db.create_all()



# do I need to add a for loop which allows users to add a flashcard?:

for idx in range(10):
    username = f"user_{idx}"
    password = f"test{idx}"
    email = f"user{idx}@test.com"
    phone = f"555-555-{idx}"
    

    db_user = crud.create_user(username, password, email, phone)
    model.db.session.add(db_user)

math_category = crud.create_category(f"math")
vocabulary_category = crud.create_category(f"vocabulary")

model.db.session.add(math_category)
model.db.session.add(vocabulary_category)

    # for _ in range(10): #what should go in the function
    #     random_flashcard = choice(flashcards_in_db)
    #     front = () #does the frontcard input text go here?
    #     back = () #does the backcard input text go here?


        # flashcard = crud.create_flashcard(front, back, random_flashcard.flashcard_id, db_user.user_id)
        # model.db.session.add(flashcard)

model.db.session.commit()


with open('data/flashcards.json') as f:
    flashcards = json.loads(f.read())

flashcards_in_db = []

for flashcard in flashcards:
    front_card, back_card, category_id, user_id = (
        flashcard["front_card"],
        flashcard["back_card"],
        flashcard["category_id"],
        flashcard["user_id"])

    db_flashcard = crud.create_flashcard(front_card, back_card, category_id, user_id)
    # print(db_flashcard)
    flashcards_in_db.append(db_flashcard) #is db_flashcard referenced correctly?

    model.db.session.add_all(flashcards_in_db)
    model.db.session.commit()
