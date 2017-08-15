# import the Flask class from the flask module
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, g
from functools import wraps
from wtforms import Form, BooleanField, StringField, PasswordField, validators

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, distinct, text

env = 'DEV'

# create the application object
app = Flask(__name__)

# config
import os
#app.config.from_object('config.BaseConfig')
conf = {
    'DEV': 'config.DevelopmentConfig',
    'PROD': 'config.CloudConfig'
}
os.environ['APP_SETTINGS'] = conf[env]
app.config.from_object(os.environ['APP_SETTINGS'])
user_table_name = app.config.get('USER_TABLE_NAME')

db = SQLAlchemy(app)
from model import *

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


# use decorators to link the function to a url
@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # return "Hello, World!"  # return a string
    #g.db = sqlite3.connect(app.database)
    # cur = g.db.execute('select * from posts')
    #
    # posts = []
    # for row in cur.fetchall():
    #     posts.append(dict(title=row[0], description=row[1]))

    # posts = [dict(title=row[0], description=row[1]) for row in cur.fetchall()]

#    g.db.close()
#    return render_template('index.html', posts=posts)  # render a template



    users = db.session.query(RegisteredUser).all()
    watchlist = db.session.query(WatchlistPeople).all()

    watchlist_name = [item.name for item in watchlist]
    watchlist_addr = [item.address for item in watchlist]

    all_match = None

    if request.method == 'POST':
        form_name = request.form['name']
        form_address = request.form['address']

        watchlist_table = WatchlistPeople.__tablename__

        name_match_query = db.session.execute("select * from {0} where name='{1}' ".format(watchlist_table, form_name))
        name_match = [(row[1],row[2]) for row in name_match_query.fetchall()]

        addr_match_query = db.session.execute("select * from {0} where address='{1}' ".format(watchlist_table, form_address))
        addr_match = [(row[1],row[2]) for row in addr_match_query.fetchall()]

        # The relationship between name match and address match is "OR" relationship
        all_match = list(name_match)
        all_match.extend(addr_match)
        all_match = list(set(all_match))

    if all_match:
        return render_template('index.html', users=users, matches = all_match)  # render a template with matches
    else:
        return render_template('index.html', users=users)  # render a template without match


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
#    if session['logged_in']:
    if 'logged_in' in session:
        flash('You were already logged in.')
        return redirect(url_for('home'))

    if request.method == 'POST':
        form_username = request.form['username']
        form_password = request.form['password']
        username_exist_count = db.session.execute(text("SELECT count(*) FROM {0} WHERE username = '{1}' AND password = '{2}'"\
            .format(user_table_name, form_username, form_password))).fetchall()[0][0]
        # print(username_exist_count)
        user_exist = True if username_exist_count >=1 else False
        if not user_exist:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET','POST'])
def signup():
    error = None
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        # Add a new user, the user id is the current max(user.id) + 1
        num_of_users = db.session.query(func.count(distinct(RegisteredUser.id))).all()[0][0]
        db.session.add(RegisteredUser(num_of_users + 1, form.username.data, form.password.data, form.email.data))
        db.session.commit()
        flash('Thanks for signing up')
        return redirect(url_for('login'))

#    print(form.username.data)
#    print(type(form.username))
#    print(form.username['value'])
    return render_template('signup.html', form = form)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
