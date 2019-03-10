import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Route, withRouter } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import Login from './components/Login';
import Footer from './components/Footer'

import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <div>
          <Route exact={true} path="/" component={Dashboard}/>
          <Route path="/callback" component={Login}/>
        </div>
        <Footer><a href="https://github.com/joshualoehr/spotify-tag-manager">GitHub</a></Footer>
      </div>
    );
  }
};

const mapStateToProps = state => {
  return state;
};

export default withRouter(connect(mapStateToProps)(App));
