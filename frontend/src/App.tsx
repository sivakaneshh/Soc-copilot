import React from 'react';
import './App.css';
import ChatBox from './components/chatbot';
import Home from './pages/home';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>SIEMplify</h1>
        <p>Your AI-powered Security Operations Center Assistant</p>
      </header>
      <main>
        <Home />
      </main>
    </div>
  );
}

export default App;
