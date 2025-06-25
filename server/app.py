from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Message
from config import Config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages])

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    try:
        message = Message(
            body=data['body'],
            username=data['username']
        )
        db.session.add(message)
        db.session.commit()
        return jsonify(message.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()
    try:
        if 'body' in data:
            message.body = data['body']
        db.session.commit()
        return jsonify(message.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    try:
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'Message deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=5555)