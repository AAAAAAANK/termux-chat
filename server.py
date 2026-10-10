from flask import Flask, request
import hashlib
import sqlite3

app = Flask(__name__)

messages = []
update = []
def get_db():
    return sqlite3.connect("chat.db")
with get_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL
        )
    """)
@app.route("/")
def home():
    return "Termux Chat Server läuft!"

@app.route("/send", methods=["POST"])
def getuser():
    secret_ID = request.json["ID_niemandem_verraten"]
    if hashlib.sha256(secret_ID.encode()).hexdigest() == "f296cd5057b67f27a2ffd4a113819366d2aaca7b65b146805a011a733d512d8c":
        return send("ELIA: ")
    elif hashlib.sha256(secret_ID.encode()).hexdigest() == "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08":
        return send("LEON :")
    else:
        return {"status": "invalid ID"}
    
def send(user):
    message = request.json["message"]

    with get_db() as db:
        db.execute(
            "INSERT INTO messages (message) VALUES (?)",
            (user + message,)
        )

    return {"status": "ok"}


@app.route("/messages")
def get_messages():
    with get_db() as db:
        rows = db.execute(
            "SELECT message FROM messages ORDER BY id"
        ).fetchall()

    return {"messages": [row[0] for row in rows]}
    

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
