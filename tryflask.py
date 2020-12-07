from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/") #url endpoint
def hello():
    return jsonify({"about":"hellllloooooo"})

if __name__ == '__main__':
    app.run(debug=True)
    