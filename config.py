from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = '9f4c5b7d9a2c4e8b6d5f3a1e7c4b6a8d'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///consultant.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app