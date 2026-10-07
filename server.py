from flask import Flask, request
import hashlib

app = Flask(__name__)

messages = []
update = []
@app.route("/")
def home():
    return "Termux Chat Server läuft!"

@app.route("/send", methods=["POST"])
def getuser():
    secret_ID = request.json["ID_niemandem_verraten"]
    if hashlib.sha256(secret_ID.encode()).hexdigest() == "HIERFÜGEICHSPÄTERELIASHASHEIN":
        return send("ELIA: ")
    elif hashlib.sha256(secret_ID.encode()).hexdigest() == "HIERFÜGEICHSPÄTERMEINENHASHEIN":
        return send("LEON :")
    else:
        return {"status": "invalid ID"}
def send(user):
    message = request.json["message"]
    messages.append(user + message)
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
    update.clear()
    return {"status": "cleared"}
    

@app.route("/clear", methods=["POST"])
def clear():
    messages.clear()
    return {"status": "cleared"}

app.run(host="0.0.0.0", port=8080)
