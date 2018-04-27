import React, { Component } from 'react';
import logo from './logo_umg.png';
import logo_alpha from './logo_alph.png';
import './App.css';

class App extends Component {
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
              <form className="cooltext">
                <input className=" cooltext cooltextinput" type="text" name="name" />
            </form>
            </div>
          </div>
        </p>
      </div>
    );
  }
}

export default App;
