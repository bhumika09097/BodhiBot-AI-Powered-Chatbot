from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# GROQ CLIENT
client = Groq(
    api_key=os.getenv("API_KEY")
)

@app.route("/")
def home():
    return render_template("index.html")

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

if __name__ == "__main__":
    app.run(debug=True)