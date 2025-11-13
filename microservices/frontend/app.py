from flask import Flask, render_template_string, jsonify
import requests

app = Flask(__name__)

TEMPLATE = """
<html>
  <head><title>Frontend Service</title></head>
  <body>
    <h2>Microservices Observables Demo</h2>
    <button onclick="fetchData()">Get Protected Data</button>
    <pre id="output"></pre>
    <script>
      async function fetchData() {
        const res = await fetch('/api');
        const data = await res.json();
        document.getElementById('output').textContent = JSON.stringify(data, null, 2);
      }
    </script>
  </body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(TEMPLATE)

@app.route("/api")
def api_proxy():
    try:
        # Demo: obtiene token y hace request a la API
        login = requests.post("http://auth:5000/login", json={"username": "admin", "password": "password"}).json()
        token = login.get("token")
        if not token:
            return jsonify({"error": "Auth failed"}), 403
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.get("http://api:5001/data", headers=headers)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "frontend service running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
