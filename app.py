from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    contacts = db.Column(db.Text)  # Store contacts as JSON or CSV format

# Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

# Gift Wishlist model
class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    occasion = db.Column(db.String(200), nullable=False)
    gift_preferences = db.Column(db.Text, nullable=False)  # Store as JSON or text format

# Movie Plans model
class MoviePlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    platform = db.Column(db.String(100), nullable=False)  # Theatre or OTT
    movie_name = db.Column(db.String(200), nullable=False)
    additional_notes = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

# Outing Plans model
class OutingPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    food_preferences = db.Column(db.Text, nullable=True)  # JSON or text format
    budget = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

# Create tables
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def home():
    return render_template('index.html')
# Permissions Page
@app.route('/permissions')
def permissions():
    return render_template('permissions.html')

# Event Wishlist Route
@app.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        occasion = request.form['occasion']
        gift_preferences = request.form['gift_preferences']
        wishlist_entry = Wishlist(user_id=session['user_id'], occasion=occasion, gift_preferences=gift_preferences)
        db.session.add(wishlist_entry)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('wishlist.html')

# View Wishlists
@app.route('/view_wishlists')
def view_wishlists():
    wishlists = Wishlist.query.all()
    return render_template('view_wishlists.html', wishlists=wishlists)

# Movie Plans Route
@app.route('/movie_plan', methods=['GET', 'POST'])
def movie_plan():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        platform = request.form['platform']
        movie_name = request.form['movie_name']
        additional_notes = request.form['additional_notes']
        movie_entry = MoviePlan(user_id=session['user_id'], platform=platform, movie_name=movie_name, additional_notes=additional_notes)
        db.session.add(movie_entry)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('movie_plan.html')

# View Movie Plans
@app.route('/view_movie_plans')
def view_movie_plans():
    movie_plans = MoviePlan.query.all()
    return render_template('view_movie_plans.html', movie_plans=movie_plans)

# View Outing Plans with Best Food Spots
@app.route('/best_food_spots')
def best_food_spots():
    return render_template('best_food_spots.html')  # Add restaurant/street food options here


# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        return 'Invalid Credentials'
    return render_template('login.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# Outing Plan route
@app.route('/outing_plan', methods=['GET', 'POST'])
def outing_plan():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        location = request.form['location']
        food_preferences = request.form['food_preferences']
        budget = request.form['budget']
        outing_entry = OutingPlan(user_id=session['user_id'], location=location, food_preferences=food_preferences, budget=budget)
        db.session.add(outing_entry)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('outing_plan.html')

# View Outing Plans
@app.route('/view_outing_plans')
def view_outing_plans():
    outing_plans = OutingPlan.query.all()
    return render_template('view_outing_plans.html', outing_plans=outing_plans)

if __name__ == '__main__':
    app.run(debug=True)
