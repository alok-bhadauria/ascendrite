import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';
import LandingPage from './pages/LandingPage';

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col justify-between bg-theme-bg text-theme-text transition-all duration-200">
        <Navbar />
        <Routes>
          <Route path="/" element={<LandingPage />} />
        </Routes>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
