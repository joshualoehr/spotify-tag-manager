import requests

SPOTIFY_API_URL = 'https://api.spotify.com/v1'

tokens_cache = {}

def spotify_post(path, data):
    headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
    response = requests.post(path, headers=headers, data=data)
    print('EXT POST %s - %s' % (path, str(response.status_code)))
    return response.json()

def spotify_get(path, dao, user_id=None, access_token=None):
    access_token = access_token or get_access_token(dao, user_id)

    if not path.startswith('https://api.spotify.com/v1'):
        path = '%s/%s' % (SPOTIFY_API_URL, path)

    response = requests.get(path, headers={'Authorization': 'Bearer %s' % access_token})
    print('EXT GET %s - %s' % (path, str(response.status_code)))
    return response.json()

def get_access_token(dao, user_id):
    if user_id in tokens_cache:
        return tokens_cache[user_id]

    access_token = dao.get_user_access_token(user_id)
    tokens_cache[user_id] = access_token
    return access_token
    