from pymongo import MongoClient, ReplaceOne

EXCLUDE_ID = { '_id': 0 }

def new_default_connection():
    return DAO('mongodb://localhost:27017/')

class DAO:

    def __init__(self, conn_url):
        _conn = MongoClient(conn_url)
        _db = _conn['stags']
        self._users = _db['users']
        self._users_auth = _db['users_auth']
        self._tracks = _db['tracks']
        self._playlists = _db['playlists']

    def get_user(self, user_id):
        return self._users.find_one({ 'user_id': user_id }, EXCLUDE_ID)

    def get_user_access_token(self, user_id):
        user = self.get_user(user_id) or {}
        return user.get('access_token')

    def get_user_tracks(self, user_id):
        return [dict(document) for document in self._tracks.find({ 'user_id': user_id }, EXCLUDE_ID)]

    def get_user_playlists(self, user_id):
        return [dict(document) for document in self._playlists.find({ 'user_id': user_id }, EXCLUDE_ID)]

    def get_playlist_tracks(self, playlist_id):
        return [dict(document) for document in self._tracks.find({ 'playlist_id': playlist_id }, EXCLUDE_ID)]

    def save_new_user_session(self, user_id, access_token, refresh_token):
        self._users.update_one(
            { 'user_id': user_id }, 
            { '$set': { 'access_token': access_token, 'refresh_token': refresh_token } }, 
            upsert=True
        )

    def save_user_playlists(self, user_id, playlists):
        requests = [ReplaceOne({ 'id': playlist['id'] }, playlist, upsert=True) for playlist in playlists]
        self._playlists.bulk_write(requests)

    def save_user_tracks(self, user_id, tracks):
        requests = [ReplaceOne({ 'id': track['id'] }, track, upsert=True) for track in tracks]
        self._tracks.bulk_write(requests)
        