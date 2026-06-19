from flask import Flask, render_template, request, jsonify, url_for
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

@app.route("/chat", methods=["POST"])
def chat():

    if "messages" not in session:
        session["messages"] = []

    user_message = request.json.get("message")

    if "user_id" in session and "conversation_id" not in session:
        conversation = Conversation(
            user_id=session["user_id"],
            title=user_message[:50]
        )

        db.session.add(conversation)
        db.session.commit()

        session["conversation_id"] = conversation.id

    if "user_id" in session:

        user_msg = Message(
            user_id=session["user_id"],
            conversation_id=session["conversation_id"],
            role="user",
            content=user_message
        )

        db.session.add(user_msg)
        db.session.commit()

    session["messages"].append({
    "role": "user",
    "content": user_message
    })

    try:

        completion = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=session["messages"],

            temperature=0.7,
            max_tokens=1024
        )
        
        bot_reply = completion.choices[0].message.content

        if "user_id" in session:
            assistant_msg = Message(
                user_id=session["user_id"],
                conversation_id=session['conversation_id'],
                role="assistant",
                content=bot_reply
            )

            db.session.add(assistant_msg)
            db.session.commit()

        session["messages"].append({
        "role": "assistant",
        "content": bot_reply
        })

    except Exception as e:

        print(e)

        bot_reply = "⚠️ BodhiBot is busy right now."

    return jsonify({
        "reply": bot_reply
    })

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

@app.route("/new_chat")
def new_chat():

    session.pop("messages", None)
    session.pop("conversation_id", None)

    return redirect(url_for("home"))

@app.route("/messages")
def messages():
    all_messages = Message.query.all()

    result = []

    for msg in all_messages:
        result.append({
            "id": msg.id,
            "user_id": msg.user_id,
            "role": msg.role,
            "content": msg.content
        })

    return jsonify(result)

@app.route("/conversations")
def conversations():

    if "user_id" not in session:
        return jsonify([])

    chats = Conversation.query.filter_by(
        user_id=session["user_id"]
    ).order_by(Conversation.id.desc()).all()

    result = []

    for chat in chats:
        result.append({
            "id": chat.id,
            "title": chat.title
        })

    return jsonify(result)

@app.route("/conversation/<int:conversation_id>")
def get_conversation(conversation_id):

    if "user_id" not in session:
        return jsonify([])

    messages = Message.query.filter_by(
        conversation_id=conversation_id
    ).all()

    result = []

    for msg in messages:
        result.append({
            "role": msg.role,
            "content": msg.content
        })

    return jsonify(result)

@app.route("/set_conversation/<int:conversation_id>")
def set_conversation(conversation_id):

    session["conversation_id"] = conversation_id

    return jsonify({"success": True})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

class Conversation(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
    title = db.Column(
        db.String(200),
        nullable=True
    )
class Message(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
    
    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey('conversation.id'),
        nullable=False
    )

    role = db.Column(db.String(20), nullable=False)

    content = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
