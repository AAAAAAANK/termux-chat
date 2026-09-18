from flask import Flask, request

app = Flask(__name__)

messages = []

@app.route("/")
def home():
    return "Termux Chat Server läuft!"

@app.route("/send", methods=["POST"])
def send():
    message = request.json["message"]
    messages.append(message)
    return {"status": "ok"}

@app.route("/messages")
def get_messages():
    return {"messages": messages}

app.run(host="0.0.0.0", port=8080)
