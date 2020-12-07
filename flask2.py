from flask import Flask, jsonify, request 

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def index():
    if (request.method == 'POST'):
        some_json = request.get_json()
        return jsonify({'you_sent':some_json}), 201
    else:
        return jsonify({'about':'hello world'})


