from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__, template_folder='templates')

# Configure the database URI and secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisissecret1234@!@#!@'

# Initialize the SQLAlchemy instance
db = SQLAlchemy(app)

# Define the User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/personalised')
def diet():
    return render_template('diet-plan.html')

@app.route('/nutrition')
def nutrition():
    return render_template('nutrition.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/about_us')
def aboutus():
    return render_template('about-us.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')


if __name__ == "__main__":
    app.run(debug=True, port= 5500)
