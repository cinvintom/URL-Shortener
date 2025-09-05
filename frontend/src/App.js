import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './index.css';
import UrlShortener from './components/UrlShortener';

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<UrlShortener />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
