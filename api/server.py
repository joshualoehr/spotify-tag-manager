from flask import Flask
from flask import request
from flask_cors import CORS

from controller import Controller
from dao import new_default_connection
from router import *

app = Flask(__name__)
CORS(app)

with open('../creds.json') as creds_file:
    creds = json.load(creds_file)

dao = new_default_connection()
controller = Controller(creds, dao)

@app.route('/login')
def login():
    code = request.args.get('code')
    err, user_id = controller.get_spotify_tokens(code)
    return json.dumps({ 'error': err } if err else { 'user_id': user_id })

@app.route('/user/<user_id>/tracks')
def get_all_tracks(user_id):
    err, tracks = controller.get_all_user_tracks(user_id)
    return json.dumps({ 'error': err } if err else { 'tracks': tracks })
