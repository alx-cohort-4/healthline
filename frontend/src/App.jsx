import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Nav from './pages/Nav';
import HeroSection from './pages/HeroSection';

const App = () => {
  return (
    <Router>
      <div className="min-h-screen">
        <Nav />
        <Routes>
          <Route path="/" element={<Navigate to="/hero" replace />} />
          <Route path="/hero" element={<HeroSection />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;