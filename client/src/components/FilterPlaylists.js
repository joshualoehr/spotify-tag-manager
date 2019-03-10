import React, { Component } from 'react';
import Select from 'react-select';
import { connect } from 'react-redux';

import { fetchPlaylists, playlistsFilter } from '../actions';

class FilterPlaylists extends Component {

    constructor(props) {
        super(props);
        const { dispatch, playlists, userID } = props;
        if (userID && playlists.length === 0) {
            dispatch(fetchPlaylists(userID));
        }
    }

    render() {
        const { dispatch, playlists, selectedPlaylists } = this.props;

        let options = playlists.map(p => {
            return { label: p.name, value: p.id }
        });
        let selected = selectedPlaylists.map(p => {
            return { label: p.name, value: p.id }
        });

        return (
            <Select
                onChange={(selected, action) => {
                    dispatch(playlistsFilter(selected));
                }}
                options={options}
                isMulti={true}
                value={selected}
            />
        );
    }
}

const mapStateToProps = state => {
    const { dispatch, playlists, selectedPlaylists, userID } = state;
    return {
        dispatch: dispatch,
        playlists: playlists,
        selectedPlaylists: selectedPlaylists,
        userID: userID
    };
}

export default connect(mapStateToProps)(FilterPlaylists);