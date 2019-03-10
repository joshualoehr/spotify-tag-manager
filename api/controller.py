import utils

# All transform functions should be stateless and idempotent
def transform_playlist(playlist, metadata={}):
    return {
        'id': playlist['id'],
        'name': playlist['name'],
        'href': playlist['href'],
        'tracks': playlist['tracks'],
        **metadata
    }

def transform_track(track, metadata={}):
    # TODO: add parsing for track['album'] -- https://developer.spotify.com/documentation/web-api/reference/object-model/#album-object-simplified
    # TODO: add parsing for track['artists'] -- https://developer.spotify.com/documentation/web-api/reference/object-model/#artist-object-simplified
    if 'track' in track:
        track = track['track']
    return {
        'id': track['id'],
        'title': track.get('title') or track.get('name'),
        'artist': 'todo',
        'album': 'todo',
        'date_added': '3/3/2018',
        'duration': '0:00',
        'popularity': track['popularity'],
        **metadata
    }

# All Controller methods (except the constructor) should return a tuple
# containing any errors (or None), and the requested resource (or None)
class Controller:

    def __init__(self, creds, dao):
        self._creds = creds
        self._dao = dao

    def get_spotify_tokens(self, code):
        response = utils.spotify_post(self._creds['TOKEN_URI'], {
            'grant_type': self._creds['GRANT_TYPE'], 
            'code': code, 'redirect_uri': self._creds['REDIRECT_URI'], 
            'client_id': self._creds['CLIENT_ID'], 
            'client_secret': self._creds['CLIENT_SECRET']
        })
        if 'error' in response:
            return response['error'], None

        access_token = response['access_token']
        refresh_token = response['refresh_token']
        response = utils.spotify_get('me', self._dao, access_token=access_token)
        if 'error' in response:
            return response['error'], None

        user_id = response['id']
        self._dao.save_new_user_session(**{
            'user_id': user_id,
            'access_token': access_token,
            'refresh_token': refresh_token
        })

        return None, user_id

    def get_all_user_tracks(self, user_id):
        tracks = self._dao.get_user_tracks(user_id)
        if tracks:
            return None, tracks

        return self.import_all_user_tracks(user_id)
    
    def import_all_user_tracks(self, user_id):
        err, playlists = self.get_all_user_playlists(user_id)
        if err:
            return err, None
        
        errs, all_tracks = [], []
        for playlist in playlists:
            err, tracks = self.get_playlist_tracks(user_id, playlist)
            if err:
                errs.append(err)
                continue

            for track in tracks:
                all_tracks.append(transform_track(track, metadata={
                    'user_id': user_id,
                    'playlist_id': playlist['id'],
                    'playlist_name': playlist['name']
                }))

        self._dao.save_user_tracks(user_id, all_tracks)
        return errs or None, all_tracks

    def get_all_user_playlists(self, user_id):
        playlists = self._dao.get_user_playlists(user_id)
        if playlists:
            return None, playlists
        
        return self.import_all_user_playlists(user_id)

    def import_all_user_playlists(self, user_id):
        response = utils.spotify_get('me/playlists', self._dao, user_id=user_id)
        if 'error' in response:
            return response['error'], None

        playlists = response['items']
        playlists = [transform_playlist(playlist, { 'user_id': user_id }) for playlist in playlists]
        self._dao.save_user_playlists(user_id, playlists)
        return None, playlists

    def get_playlist_tracks(self, user_id, playlist):
        tracks = self._dao.get_playlist_tracks(playlist['id'])
        if tracks:
            return None, tracks

        return self.import_playlist_tracks(user_id, playlist)

    def import_playlist_tracks(self, user_id, playlist):
        response = utils.spotify_get(playlist['tracks']['href'], self._dao, user_id=user_id)
        if 'error' in response:
            return response['error'], None

        tracks = response['items']
        tracks = [transform_track(track) for track in tracks]
        self._dao.save_user_tracks(user_id, tracks)
        return None, tracks
