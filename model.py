from wtforms import Form, BooleanField, StringField, PasswordField, validators
from app import db


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
#    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

class RegisteredUser(db.Model):

    __tablename__ = "registered_user"

    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    email = db.Column(db.Text)

    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

class WatchlistPeople(db.Model):

    __tablename__ = "watchlist_people"
    id = db.Column(db.BigInteger, primary_key = True)
    name = db.Column(db.Text)
    address = db.Column(db.Text)

    def __init__(self, name, address):
        self.id = id
        self.name = name
        self.address = address

    def __repr__(self):
        return '<Watchlist_Person %r>' % self.name
