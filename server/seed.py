from app import app
from models import db, Message

with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()

    # Seed initial messages
    messages = [
        Message(body="Hello, world!", username="User1"),
        Message(body="Flask is awesome!", username="User2"),
        Message(body="Learning full-stack development", username="User3"),
    ]

    db.session.add_all(messages)
    db.session.commit()
    print("Database seeded!")