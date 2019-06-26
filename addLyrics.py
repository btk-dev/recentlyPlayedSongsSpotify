import auths
import dblayer
from lyrics_extractor import Song_Lyrics
#from PyLyrics import *

tracks = []
artists = []

index = 0

f = open("lyrics.txt","a+")

dblayer.opendb('music_history')

dblayer.getAllEntries()

tracks = dblayer.returnTracks()
artists = dblayer.returnArtists()

for track in tracks:
    #f.write(PyLyrics.getLyrics(artists[index], tracks[index]))
    #index = index + 1
    extract_lyrics = Song_Lyrics(auths.apiEngineKey, auths.engineID)
    song_title, song_lyrics = extract_lyrics.get_lyrics(track)
    f.write(song_lyrics)
