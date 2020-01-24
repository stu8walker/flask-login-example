from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

# 
app = Flask(__name__)

# Set the secret key
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


# Forms



# Routes
@app.route('/', methods=['GET'])
def index():
    return "Index Page"

@app.route('/login', methods=['GET', 'POST'])
def login():
    return "Login Page"

@app.route('/register', methods=['GET', 'POST'])
def register():
    return "Register Page"

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return "Hello " + current_user.firstname

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))


# Run app
if __name__ == '__main__':
    app.run()
  