from cloudant.client import CouchDB
from cloudant.document import Document
import auths

couchUsername = auths.couchUsername
couchpw = auths.couchPassword

client = CouchDB(couchUsername, couchpw , url='http://127.0.0.1:5984', connect=True)

my_database = client['music_history']

session=client.session()
print('Username: {0}'.format(session['userCtx']['name']))
print('Databases: {0}'.format(client.all_dbs()))

def opendb(dbname):
    my_database = client[dbname]
    print("SUCCESS")

def checkIfEntryExists(entryID):
    doc_exists = entryID in my_database

    if doc_exists:
        #get doc revision number and increase number of times listened to
        my_document = my_database[entryID]
        my_document['numListens'] += 1
        my_document.save()
        return True
    else:
        return False

def addEntry(song):
    data = { '_id': song.sid,
            'track_name': song.name,
            'artist': song.artist,
            'duration': song.duration,
            'explicit': song.explicit,
            'preview_url': song.previewUrl,
            'track_number': song.trackNumber,
            'numListens': song.numListens,
            'features': {
                'duration': song.features.duration,
                'key': song.features.key,
                'mode': song.features.mode,
                'time_signature': song.features.timeSig,
                'danceability': song.features.danceability,
                'energy': song.features.energy,
                'instrumentalness': song.features.instrumentalness,
                'liveness': song.features.liveness,
                'loudness': song.features.loudness,
                'speechiness': song.features.speechiness,
                'valence': song.features.valence,
                'tempo': song.features.tempo
                }#,
            #'analysis': {
            #    'bars': {
             #       'start': song.analysis.bars['start'],
              #      'duration': song.analysis.bars['duration'],
               #     'confidence': song.analysis.bars['confidence']
                #    },
           #     'beats': {
            #        'start': song.analysis.beats['start'],
             #       'duration': song.analysis.beats['duration'],
              #      'confidence': song.analysis.beats['confidence']
               #     },
                #'sections': {
         #           'start': song.analysis.sections['start'],
          #          'duration': song.analysis.sections['duration'],
           #         'confidence': song.analysis.sections['confidence'],
            #        'loudness': song.analysis.sections['loudness'],
             #       'tempo': song.analysis.sections['tempo'],
              #      'tempo_confidence': song.analysis.sections['tempo_confidence'],
               #     'key': song.analysis.sections['key'],
                #    'key_confidence': song.analysis.sections['key_confidence'],
                 #   'mode': song.analysis.sections['mode'],
                  #  'mode_confidence': song.analysis.sections['mode_confidence'],
                   # 'time_signature': song.analysis.sections['time_signature'],
           #         'time_signature_confidence': song.analysis.sections['time_signature_confidence']
            #        },
             #   'segments': {
              #      'start': song.analysis.segments['start'],
               #     'duration': song.analysis.segments['duration'],
                #    'confidence': song.analysis.segments['confidence'],
                 #   'loudness_start': song.analysis.segments['loudness_start'],
                  #  'loudness_max_time': song.analysis.segments['loudness_max_time'],
                   # 'loudness_max': song.analysis.segments['loudness_max'],
         #           'loudness_end': song.analysis.segments[']loudness_end'],
          #          'pitches': song.analysis.segments['pitches'],
           #         'timbre': song.analysis.segments['timbre']
            #        },
             #   'tatums': {
              #      'start': song.analysis.tatums['start'],
               #     'duration': song.analysis.tatums['duration'],
                #    'confidence': song.analysis.tatums['confidence']
                 #   }
               # }
            }
    my_document = my_database.create_document(data)

    if my_document.exists():
        print('SUCCESS')

def getAllEntries():
    for document in my_database:
        for document in my_database:
            print(document)

def closeConnection():
    client.disconnect()
