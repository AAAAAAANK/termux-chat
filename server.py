from flask import Flask, request

app = Flask(__name__)

messages = []
update = []
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

@app.route("/sendupdate", methods=["POST"])
def uploadupdate():
    update.clear()
    script = request.json["script"]
    update.append(script)
    return {"status": "uploaded"}


@app.route("/getupdate")
def download_update():
    return {"update": update}

@app.route("/clearupdate")
def clear_update():
    update.clear
    return {"status": "cleared"}
    

@app.route("/clear", methods=["POST"])
def clear():
    messages.clear()
    return {"status": "cleared"}

app.run(host="0.0.0.0", port=8080)
