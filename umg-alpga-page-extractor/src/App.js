import React, { Component } from 'react';
import logo from './logo_umg.png';
import logo_alpha from './logo_alph.png';
import './App.css';

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      title: null
    }
    this.apiCall = this.apiCall.bind(this);
    this.setTitle = this.setTitle.bind(this);
  }

  _handleKeyPress(e) {
    if (e.key === 'Enter') {
      this.apiCall(e.target.value, this);
    }
  }

  setTitle(title) {
    console.log(title)
  }

  apiCall(URL, x){
    fetch('http://localhost:5000/extract?url='+URL, {mode: 'cors'})
      .then(
        function(response) {
          response.json().then(function(data) {
            console.log(data[0]);
            x.setState({
              title: data[0].title
            });
          });
        }
      )
      .catch(function(err) {
        console.log('Fetch Error :-S', err);
      });
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <div>
            <h1 className="App-title">Universal Music & Alpha</h1>
            <h2 className="App-title">present</h2>
            <h3 className="App-title">Press Source Data Extraction Tool</h3>
            <h4 className="App-title">#musicathon</h4>
          </div>
          <img src={logo_alpha} className="App-logo" alt="logo" />
        </header>
        <p className="App-intro">
          <div className="slide">
            <div className="slide-inner">
              <div className="cooltext">
                <input onKeyPress={this._handleKeyPress.bind(this)} className=" cooltext cooltextinput" type="text" name="name" />
            </div>
            {this.state.title?
              <h6>{this.state.title}</h6>
               : null}
            </div>
          </div>
        </p>
      </div>
    );
  }
}

export default App;
