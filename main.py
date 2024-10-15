from flask import Flask, redirect, request, url_for, session
import spotipy import spotify
from spotipy import oauth2
import time
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = 'http://127.0.0.1:5000/redirect'
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'


def create_spotify_auth():
    return oauth2(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        redirect_uri = url_for('redirect'), _external = True,
        scope = 'user-library-read'
    )

@app.route('/login')
def login():
    auth_url = create_spotify_auth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify.auth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('recentListen', external = True))

@app.route('/recentListen')

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        redirect(url_for('login', external = False))
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if(is_expired):
        spotify_auth = create_spotify_auth()
        token_info = spotify_auth.refresh_access_token(token_info['refresh_token'])

    return token_info

app.run(debug=True)
