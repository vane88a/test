from flask import Flask, jsonify, request, make_response, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import jwt 
import datetime
from functools import wraps

app = Flask(__name__)

#for jwtoken
app.config['SECRET_KEY'] = 'thisisthesecretkey'


#1 login and authentication .
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #http://127.0.0.1:5000/route?token=alshfjfjdklsfj89549834ur

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403
	
	#verify that token is valid		
        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated

@app.route('/unprotected')
def unprotected():
    return jsonify({'message' : 'Anyone can view this!'})

@app.route('/protected')
@token_required #intialising requirement of token
def protected():
    return jsonify({'message' : 'This is only available for people with valid tokens.'})

@app.route('/login')
def login():
    auth = request.authorization

    #to see if user has credential to login to page 
    if auth and auth.password == 'secret':
        #creating token
        token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=3)}, app.config['SECRET_KEY']) #giving an expiry to token 
        prompt_time =  datetime.datetime.utcnow() +  datetime.timedelta(minutes=2) # last one min prompt to extend session
        #session.permanent = True

        if (datetime.datetime.utcnow() == prompt_time): #at the last 1 minute1 of the session, call function extend session
            # jsonify({'message' : 'restart!'})
            restart_session()
        else:
            return jsonify({'token' : token.decode('UTF-8')}) #deconde to regular string. returning the token so to retrieve data from server. 
        #return redirect(url_for('index')) #redirect to subsequent pages

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

#restart session
@app.route('/', methods =['GET'])
def restart_session():
    #check if user needs  
    default_opt = False
    user_choice = request.form.get('extension', default_opt)
    if (user_choice == True): #if user choose to restart, create new token.
        #token = requests.get('xxxx')
        #token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=15)}, app.config['SECRET_KEY']) #giving an expiry to token 
        flask.session.modified = True
        return Token


#fill up form - validate and put into db 
# retrieve from db
    






if __name__ == '__main__':
    app.run(debug=True)

