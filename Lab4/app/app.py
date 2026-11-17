from flask import Flask, jsonify, request

app = Flask(__name__)


@app.get("/")
def hello():
    return "Hello world from app in Docker container."


@app.get("/info")
def info():
    return jsonify({
        "lab": 4,
        "variant": 5,
        "message": "Web application is running in Docker"
    })


@app.post("/echo")
def echo():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Send a JSON object"
        }), 400

    return jsonify({
        "message": "POST request received",
        "received": data
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)