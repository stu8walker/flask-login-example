# Flask login example

Simple example of flask-login to create a registration and login system with SQLAlchemy and bootstrap 4.

Test the demo

sudo pip3 install pipenv  <br />
git clone https://github.com/stu8walker/flask-login-example.git  <br />
pipenv install  <br />
pipenv install flask flask-sqlalchemy flask-migrate flask-login flask-WTF werkzeug <br />
pipenv shell  <br />
flask shell  <br/>
from app import db  <br/>
db.create_all()  <br/>
exit()  <br/>
flask run  <br />
