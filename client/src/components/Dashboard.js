import React, { Component } from 'react';
import { Button, Nav, Jumbotron } from 'react-bootstrap';
import { connect } from 'react-redux';
import ReactTable from 'react-table';
import 'react-table/react-table.css';

import { abandonSession, fetchAuthURL, fetchPlaylists, fetchTracks } from '../actions';
import FilterPlaylists from './FilterPlaylists';

const columns = [{
    Header: 'Title',
    accessor: 'title'
}, {
    Header: 'Artist',
    accessor: 'artist'
}, {
    Header: 'Album',
    accessor: 'album'
}, {
    Header: 'Playlist',
    accessor: 'playlist_name'
}, {
    Header: 'Date Added',
    accessor: 'date_added'
}, {
    Header: 'Duration',
    accessor: 'duration'
}, {
    Header: 'Popularity',
    accessor: 'popularity'
}];

class Dashboard extends Component {

    constructor(props) {
        super(props);

        const { dispatch, authURL, userID } = this.props;
        
        if (!authURL) {
            dispatch(fetchAuthURL());
        }
        
        if (userID) {
            dispatch(fetchPlaylists(userID));
            dispatch(fetchTracks(userID));
        }

        this.signOut = () => dispatch(abandonSession());
    }

    render() {
        const { authURL, selectedPlaylists, tracks, tracksLoading, userID } = this.props;

        let selectedTracks = tracks.filter(track => {
            return selectedPlaylists.some(playlist => playlist.id === track.playlist_id);
        });

        return !userID ? (
            <div>
                <Jumbotron style={{textAlign: 'left', marginLeft: '3em', marginRight: '3em'}}>
                    <h1>Spotify Tag Manager</h1>
                    <p>This is a simple web app for managing your Spotify library with custom tags, advanced filtering, and more.</p>
                    <p>
                        <Button disabled={!authURL} href={authURL}>Connect to Spotify</Button>
                        <span style={{paddingLeft: '1em'}}>or try it out first <a href="/">with some sample data.</a></span>
                    </p>
                </Jumbotron>
            </div>
        ) : (
            <div>
                <Nav className="justify-content-end">
                    <Nav.Item><Button variant="outline-primary" onClick={this.signOut} >Sign Out</Button></Nav.Item>
                </Nav>
                <FilterPlaylists />
                <ReactTable 
                    data={selectedTracks}
                    columns={columns}
                    loading={tracksLoading}
                    filterable={true}
                />
            </div>
        );
    }
};

const mapStateToProps = (state) => state;

export default connect(mapStateToProps)(Dashboard);