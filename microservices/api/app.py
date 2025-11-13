from flask import Flask, jsonify, request
import jwt

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"

def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token missing"}), 403
        try:
            jwt.decode(token.split(" ")[1], app.config["SECRET_KEY"], algorithms=["HS256"])
        except Exception as e:
            return jsonify({"error": "Invalid token"}), 403
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route("/data", methods=["GET"])
@token_required
def data():
    return jsonify({"data": "Protected API content"})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "api service running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
