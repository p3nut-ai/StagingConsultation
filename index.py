from config import create_app
from models import *
from routes import register_routes
from werkzeug.security import generate_password_hash, check_password_hash


app = create_app()
db.init_app(app)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin1').first():
        new_user1 = User(
            username='admin1',
            password=generate_password_hash('password1'),  # Admin 1 fixed credentials
            email='admin1@example.com',
            image='static/prof1.jpg',
            role='admin'  # Role can be used for further permission management
        )
        db.session.add(new_user1)

    if not User.query.filter_by(username='admin2').first():
        new_user2 = User(
            username='admin2',
            password=generate_password_hash('password2'),  # Admin 2 fixed credentials
            email='admin2@example.com',
            image='static/prof2.jpg',
            role='admin'
        )
        db.session.add(new_user2)
    db.session.commit()    

register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)