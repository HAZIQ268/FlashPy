from flask import Flask, render_template, redirect, url_for, flash
from forms import RegisterForm, LoginForm
from models import User, users_db
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt

# Initialize app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

# Password hashing
bcrypt = Bcrypt(app)

# Login manager setup
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Load user from "database"
@login_manager.user_loader
def load_user(user_id):
    return users_db.get(user_id)

# Home route
@app.route("/")
def home():
    return redirect(url_for("login"))

# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        # Hash password
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        # Create user
        user = User(form.username.data, hashed_pw)
        
        # Save in fake DB
        users_db[form.username.data] = user
        
        flash("Account created! Please login.")
        return redirect(url_for("login"))
        
    return render_template("register.html", form=form)

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = users_db.get(form.username.data)
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password")
            
    return render_template("login.html", form=form)

# Protected route
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

# Logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

# Run app
if __name__ == "__main__":
    app.run(debug=True)