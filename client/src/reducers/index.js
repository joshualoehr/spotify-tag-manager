import { createReducer } from 'redux-starter-kit';
import * as actions from '../actions';

const savePayloadAs = (key) => (state, action) => {
    state[key] = action.payload;
}

const rootReducer = createReducer({
    authURL: localStorage.authURL || null,
    userID: localStorage.userID || null,
    playlists: [],
    selectedPlaylists: [],
    tracks: [],
    tracksLoading: false
}, {
    [actions.receiveLoginError]: savePayloadAs('error'),
    [actions.authURLReceived]: (state, action) => {
        state.authURL = action.payload;
        localStorage.authURL = action.payload;
    },
    [actions.createSession]: (state, action) => {
        state.userID = action.payload;
        localStorage.userID = action.payload;
    },
    [actions.abandonSession]: (state, action) => {
        state.userID = null;
        delete localStorage.userID;
        window.location.reload();
    },
    [actions.playlistsReceived]: (state, action) => {
        state.playlists = action.payload;
        state.selectedPlaylists = action.payload;
    },
    [actions.playlistsFilter]: (state, action) => {
        state.selectedPlaylists = action.payload.map(p => {
            return { id: p.value, name: p.label };
        });
    },
    [actions.tracksLoading]: savePayloadAs('tracksLoading'),
    [actions.tracksReceived]: savePayloadAs('tracks')
});

export default rootReducer;