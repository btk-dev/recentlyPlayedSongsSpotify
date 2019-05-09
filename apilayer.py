import requests
import json
import six
import base64
from urllib.parse import urlencode
import webbrowser
import dblayer
import auths

client_id = auths.spotifyID
client_secret = auths.spotifySecret
redirect_url = 'http://localhost:8888/callback/'
fallback_scope = 'user-read-private'
authorize_url = 'https://accounts.spotify.com/authorize'
token_url = 'https://accounts.spotify.com/api/token'

url = ('https://accounts.spotify.com/authorize/?client_id=' + client_id +'&response_type=code&redirect_uri=https%3A%2F%2Fexample.com%2Fcallback&scope=user-read-private%20user-read-email&state=34Fs29kd09')

code = ""
token = ""
song_history = []

class Song:
    def __init__(self, song_id, name):
        self.sid = song_id
        self.name = name

class Features:
    def __init__(self, sid):
        self.s = sid

class Analysis:
    def __init__(self, sid):
        self.s = sid


def parse_code(url):
    try:
        return url.split("?code=")[1].split("&")[0]
    except:
        return None

def get_authorize_url():
    payload = {'client_id': client_id,
            'response_type': 'code',
            'redirect_uri': redirect_url,
            'scope': 'user-read-recently-played'}

    urlparams = urlencode(payload)

    newurl = "%s?%s" % (authorize_url, urlparams)
    webbrowser.open(newurl)

    try:
        response = input("Enter redirected url ")
    except:
        response = input("Enter redirected url")

    code = parse_code(response)

    get_token(code)

def make_headers():
    clientID = client_id
    clientSecret = client_secret
    auth_header = base64.b64encode(six.text_type(clientID + ':' +        clientSecret).encode('ascii'))
    return {'Authorization': 'Basic %s' % auth_header.decode('ascii')}

def get_token(code):

    payload = {'redirect_uri': redirect_url,
            'code': code,
            'grant_type': 'authorization_code'}

    headers = make_headers()

    response = requests.post(token_url, data=payload, headers=headers)

    token_info = response.json()

    get_recently_played(token_info['access_token'])

def get_recently_played(token):

    playlist_url = "https://api.spotify.com/v1/me/player/recently-played/"

    headerInfo = {'content-type': 'application/json',
            'Authorization': 'Bearer %s' % token}

    response = requests.get(playlist_url, headers=headerInfo)

    res = response.json()

    for track in res['items']:
        i = track['track']['id']
        n = track['track']['name']
        s = Song(i, n)
        s.artist = track['track']['artists']
        s.duration = track['track']['duration_ms']
        s.explicit = track['track']['explicit']
        s.previewUrl = track['track']['preview_url']
        s.trackNumber = track['track']['track_number']
        s.numListens = 1
        s.features = get_features_spotify(s.sid, token)
        s.analysis = get_analysis_spotify(s.sid, token)
        song_history.append(s)

    dblayer.opendb('music_history')
    for song in song_history:
        if(dblayer.checkIfEntryExists(song.sid) == False):
            dblayer.addEntry(song)

    dblayer.closeConnection()

def get_features_spotify(track_id, token):
    features_url = "https://api.spotify.com/v1/audio-features/" + track_id

    header_info = {'content-type': 'application/json',
            'Authorization': 'Bearer %s' % token}

    feature = requests.get(features_url, headers=header_info)

    f = feature.json()

    feat = Features(track_id)

    feat.duration = f['duration_ms']
    feat.key = f['key']
    feat.mode = f['mode']
    feat.timeSig = f['time_signature']
    feat.acousticness = f['acousticness']
    feat.danceability = f['danceability']
    feat.energy = f['energy']
    feat.instrumentalness = f['instrumentalness']
    feat.liveness = f['liveness']
    feat.loudness = f['loudness']
    feat.speechiness = f['speechiness']
    feat.valence = f['valence']
    feat.tempo = f['tempo']

    return feat

def get_analysis_spotify(track_id, token):
    analysis_url = 'https://api.spotify.com/v1/audio-analysis/' + track_id

    header_info = {'content-type': 'application/json',
    'Authorization': 'Bearer %s' % token}

    analysis = requests.get(analysis_url, headers=header_info)

    a = analysis.json()

    anal = Analysis(track_id)

    anal.bars = a['bars']
    anal.beats = a['beats']
    anal.sections = a['sections']
    anal.segments = a['segments']
    anal.tatums = a['tatums']
    anal.trackInfo = a['track']

    return anal

make_headers()
get_authorize_url()
