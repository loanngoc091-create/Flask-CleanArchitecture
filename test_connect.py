from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/ping")
def ping():
    return jsonify({"msg": "pong"})

if __name__ == "__main__":
    app.run(port=9999, debug=True)
