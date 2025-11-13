from flask import Flask, request, jsonify
import jwt 
import datetime 

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "password":
        token = jwt.encode(
            { 
            "user":username,
            "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            },
            app.config["SECRET_KEY"],
            algorithm="HS256"
        )
        return jsonify({"token":token})
    return jsonify({"error":"Invalid credentials"}), 401

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status":"auth service running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)