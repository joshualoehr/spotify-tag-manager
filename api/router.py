from flask import Flask
from flask import request
from flask_cors import CORS
import json

from controller import Controller
from dao import new_default_connection

app = Flask(__name__)
CORS(app)

with open('../creds.json') as creds_file:
    creds = json.load(creds_file)
    creds['SCOPES'] = ','.join(creds['SCOPES'])

dao = new_default_connection()
controller = Controller(creds, dao)

@app.route('/auth')
def provide_auth_url():
    return json.dumps({
        'auth_url': '{AUTH_URI}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPES}'.format(**creds)
    })

@app.route('/login')
def login():
    code = request.args.get('code')
    err, user_id = controller.get_spotify_tokens(code)
    return json.dumps({ 'error': err } if err else { 'user_id': user_id })

@app.route('/user/<user_id>/tracks')
def get_all_tracks(user_id):
    err, tracks = controller.get_all_user_tracks(user_id)
    return json.dumps({ 'error': err } if err else { 'tracks': tracks })

@app.route('/user/<user_id>/playlists')
def get_all_playlists(user_id):
    err, playlists = controller.get_all_user_playlists(user_id)
    return json.dumps({ 'error': err } if err else { 'playlists': playlists })
