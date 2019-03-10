import { createAction } from 'redux-starter-kit';

const API_URL = "http://localhost:5000";

export const receiveLoginError = createAction('RECEIVE_LOGIN_ERROR');
export const authURLReceived = createAction('AUTH_URL_RECEIVED');
export const createSession = createAction('NEW_SESSION');
export const abandonSession = createAction('ABANDON_SESSION');
export const playlistsReceived = createAction('PLAYLISTS_RECEIVED');
export const playlistsFilter = createAction('PLAYLISTS_FILTER');
export const tracksReceived = createAction('TRACKS_RECEIVED');
export const tracksLoading = createAction('TRACKS_LOADING');

export const fetchAuthURL = () => dispatch => {
    return fetch(`${API_URL}/auth`)
        .then(response => response.json())
        .then(json => {
            dispatch(authURLReceived(json.auth_url));
        })
        .catch(alert);
}

export const fetchPlaylists = userID => dispatch => {
    return fetch(`${API_URL}/user/${userID}/playlists`)
        .then(response => response.json())
        .then(json => {
            dispatch(playlistsReceived(json.playlists));
        })
        .catch(alert);
}

export const fetchTokens = code => dispatch => {
    return fetch(`${API_URL}/login?code=${code}`)
        .then(response => response.json())
        .then(json => {
            dispatch(createSession(json.user_id));
        })
        .catch(alert);
};

export const fetchTracks = userID => dispatch => {
    dispatch(tracksLoading(true));
    return fetch(`${API_URL}/user/${userID}/tracks`)
        .then(response => response.json())
        .then(json => {
            dispatch(tracksReceived(json.tracks));
            dispatch(tracksLoading(false));
        })
        .catch(alert);
}