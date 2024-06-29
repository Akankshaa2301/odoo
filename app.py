from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_session import Session

app = Flask(__name__, template_folder='templates')

# Configure the database URI and secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'sdffsfshfd2651651651sfs6f416516dfs!@#6f6sf6sf'
# Initialize the SQLAlchemy instance
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    profile = db.relationship('UserProfile', uselist=False, backref='user')

# Define the UserProfile model
class UserProfile(db.Model):
    user_profile_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum('male', 'female', 'other'))
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    dietary_preferences = db.Column(db.String(255))
    allergies = db.Column(db.String(255))
    health_goals = db.Column(db.Text)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

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

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists')
            return redirect(url_for('signup'))

        # Create a new user and hash the password
        new_user = User(
            email=email,
            password_hash=generate_password_hash(password, method='pbkdf2:sha256')
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully')
        return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/health_info', methods=['POST'])
def health_info():
    if request.method == 'POST':
        age = request.form['age']
        gender = request.form['gender']
        weight = request.form['weight']
        height = request.form['height']
        diet = request.form['diet']
        allergies = request.form['allergies']
        health_goals = request.form['health-goals']

        # Assuming you have stored the user ID in session after signup or login
        user_id = session.get('user_id')

        if user_id:
            # Create or update user profile with health information
            user_profile = UserProfile.query.filter_by(user_id=user_id).first()
            if user_profile:
                # Update existing profile
                user_profile.age = age
                user_profile.gender = gender
                user_profile.weight = weight
                user_profile.height = height
                user_profile.dietary_preferences = diet
                user_profile.allergies = allergies
                user_profile.health_goals = health_goals
            else:
                # Create new profile
                new_profile = UserProfile(
                    user_id=user_id,
                    age=age,
                    gender=gender,
                    weight=weight,
                    height=height,
                    dietary_preferences=diet,
                    allergies=allergies,
                    health_goals=health_goals
                )
                db.session.add(new_profile)

            db.session.commit()
            flash('Health information updated successfully')
            return redirect(url_for('profile'))
        else:
            flash('User session expired. Please login again.')
            return redirect(url_for('personalized'))

    return render_template('diet-plan.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5500)
