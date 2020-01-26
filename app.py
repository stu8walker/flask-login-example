from flask import Flask, render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo, DataRequired
from flask_sqlalchemy  import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
import os, datetime


# Initialise Flask
app = Flask(__name__)

# Set the secret key
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# CSRF enabled globally
csrf = CSRFProtect(app)
csrf.init_app(app)

# Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    registered_date = db.Column(db.DateTime, nullable=False) # need default?
    email_confirmed = db.Column(db.Boolean, nullable=False)
    email_confirmed_date = db.Column(db.DateTime, nullable=True)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


# Forms
class RegisterForm(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired(message="Please enter your first name"), 
        Length(min=4, max=20)])
    surname = StringField('Surname', validators=[InputRequired(message="Please enter your surname"), 
        Length(min=4, max=20)])
    email = StringField('Email', validators=[InputRequired(message="Please enter your email address"), 
        Email(message="Please provide a valid email address"), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(message="Please enter a password"), 
        Length(min=8, max=80)])
    password2 = PasswordField('Repeat Password', 
        validators=[InputRequired(message="Please repeat your password"), 
        EqualTo('password', message="The passwords you entered do not match. Please try again."), 
        Length(min=8, max=80)])
    submit = SubmitField('Register')
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(message="Please enter your email address"), 
        Email(message='Please provide a valid email address')])
    password = PasswordField('Password', validators=[InputRequired(message="Please enter your password")])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# Routes
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is None or not check_password_hash(user.password, form.password.data):
            flash('Your email or password is incorrect. Please try again', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        
        # Should check if the url is safe for redirects
        # Any argument not for site should be redirected
        # e.g. 127.0.0.1:5000/login?next=http://some-malicious-site.com
        
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(first_name = form.first_name.data, surname = form.surname.data, 
                        email = form.email.data, password = hashed_password, 
                        registered_date=datetime.datetime.now(), email_confirmed=False)
        db.session.add(new_user)
        db.session.commit()
        flash('Your new account has been created! Time to login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    user = current_user.first_name
    return render_template('dashboard.html', user=user)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))


# Run app
if __name__ == '__main__':
    app.run()
  