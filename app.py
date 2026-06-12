from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect
from flask import session

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

# GROQ CLIENT
client = Groq(
    api_key=os.getenv("API_KEY")
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            session["user_id"] = user.id
            session["username"] = user.username

            return redirect("/")

        return "Invalid Email or Password"

    return render_template("login.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form.get("username")

        email = request.form.get("email")

        password = request.form.get("password")

        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            return "Passwords do not match"

        # check existing user
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "User already exists"

        # hash password
        hashed_password = generate_password_hash(password)

        # create user
        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template('signup.html')

@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json.get("message")

    try:

        completion = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ],

            temperature=0.7,
            max_tokens=1024
        )

        bot_reply = completion.choices[0].message.content

    except Exception as e:

        print(e)

        bot_reply = "⚠️ BodhiBot is busy right now."

    return jsonify({
        "reply": bot_reply
    })

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
