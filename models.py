from nxthen import db, login_manager,app
from flask_login import UserMixin

import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    is_admin = db.Column(db.Boolean, default=False)
    posts = db.relationship('Reviews', backref='author', lazy=True)


class Reviews(db.Model):
    __bind_key__= 'three'
    review_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    product_service = db.Column(db.String(100))
    review_text = db.Column(db.Text(350))
    date_posted = db.Column(db.DateTime, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

class Messages(db.Model):
    __bind_key__='four'
    message_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    issue = db.Column(db.Text(1000))

class Booking(db.Model):
    __bind_key__='five'
    booking_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)

class Report(db.Model):
    __bind_key__='seven'
    report_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    title=db.Column(db.String(50))
    report_text=db.Column(db.Text(350))
    date_posted = db.Column(db.DateTime, default=datetime.datetime.now)


db.create_all(bind="three")
db.create_all(bind="four")
db.create_all(bind="five")
db.create_all(bind="seven")


