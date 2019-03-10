import queryString from 'query-string';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Redirect, withRouter } from 'react-router-dom';
import { receiveLoginError, fetchTokens } from '../actions';

class Login extends Component {

    constructor(props) {
        super(props);

        const { dispatch, location } = this.props;
        const { code, error } = queryString.parse(location.search);

        if (code && !error) {
            dispatch(fetchTokens(code));
        } else {
            dispatch(receiveLoginError(error));
        }
    }

    render() {
        const { error, userID } = this.props;

        if (error) {
            return (
                <div className="Login">
                    <p>Error: {error}</p>
                    <a href="http://localhost:3000/">Home</a>
                </div>
            );
        } else {
            return !userID ? (
                <p>Logging in...</p>
            ) : (
                <Redirect to="/"/>
            );
        }
    };
};

const mapStateToProps = state => state;

export default withRouter(connect(mapStateToProps)(Login));