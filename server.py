from flask import Flask, request
import os
import hashlib
import psycopg2

app = Flask(__name__)

messages = []
update = []
def get_db():
    return psycopg2.connect(os.environ["DATABASE_URL"])
    
def init_db():
    db = get_db()
    try:
        cur = db.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                message TEXT NOT NULL
            )
        """)
        db.commit()
        cur.close()
    finally:
        db.close()


init_db()
@app.route("/")
def home():
    return "Termux Chat Server läuft!"

@app.route("/test")
def home2():
    return "Ja du bist ein schibidi"

@app.route("/send", methods=["POST"])
def getuser():
    secret_ID = request.json["ID_niemandem_verraten"]
    if hashlib.sha256(secret_ID.encode()).hexdigest() == "d0bd9cdbc9a7515a48d31a7ec333b19380bfe3b24f74e0f8f49c875d3a5d4170":
        return send("ELIA: ")
    elif hashlib.sha256(secret_ID.encode()).hexdigest() == "f17cedf84e97d5f67df8d010e99ea5c8588c48b2a79baf1156e86720a60b6016":
        return send("LEON(der schibidinatoer) :")
    else:
        return {"status": "invalid ID"}
    
def send(user):
    message = request.json["message"]

    db = get_db()
    try:
        cur = db.cursor()
        cur.execute(
            "INSERT INTO messages (message) VALUES (%s)",
            (user + message,)
        )
        db.commit()
        cur.close()
    finally:
        db.close()

    return {"status": "ok"}

@app.route("/messages")
def get_messages():
    db = get_db()
    try:
        cur = db.cursor()
        cur.execute("SELECT message FROM messages ORDER BY id")
        rows = cur.fetchall()
        cur.close()
    finally:
        db.close()

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
