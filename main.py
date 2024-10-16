from flask import Flask, redirect, request, url_for, session
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
import time
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:5000/callback'
scope = 'user-top-read'
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

cache_handler = FlaskSessionCacheHandler(session)

spOauth = SpotifyOAuth(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    redirect_uri = REDIRECT_URI,
    scope = scope,
    cache_handler = cache_handler,
    show_dialog = True
)


sp = Spotify(auth_manager = spOauth)

@app.route('/')
def home():
    if not spOauth.validate_token(cache_handler.get_cached_token()):
        auth_url = spOauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('get_top_songs'))

@app.route('/callback')
def callback():
    spOauth.get_access_token(request.args['code'])
    return redirect(url_for('get_top_songs'))
@app.route('/get_top_songs')
def get_top_songs():
    if not spOauth.validate_token(cache_handler.get_cached_token()):
        auth_url = spOauth.get_authorize_url()
        return redirect(auth_url)
    top_track = sp.current_user_top_tracks(limit = 10, offset = 0, time_range = 'long_term')
    top_info = [(track['name'], track['artists'][0]['name'],track['duration_ms']) for track in top_track['items']]
    session['top_info'] = top_info
    return redirect(url_for('display_top_tracks'))

def msToMinutes(ms):
    minutes = ms // 60000
    seconds = (ms % 60000) // 1000
    return f"{minutes}:{seconds:02d}"
def update_top(top_info):
    top_info = session['top_info']
    return [(name, artist, msToMinutes(duration_ms)) for name, artist, duration_ms in top_info]

@app.route('/display_top_tracks')
def display_top_tracks():
    top_info = session['top_info']
    updated = update_top(top_info)
    print(updated)
    return "testing purposes: display nothing"


    



app.run(debug=True)
