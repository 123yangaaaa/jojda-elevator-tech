import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import ElevatorRequirement from './pages/ElevatorRequirement';
import ElevatorRequirementPro from './pages/ElevatorRequirementPro';
import MaintenanceService from './pages/MaintenanceService';
import ComplaintChannel from './pages/ComplaintChannel';
import Contact from './pages/Contact';
import ElevatorDrawings from './pages/ElevatorDrawings';
import KnowledgeHub from './pages/KnowledgeHub';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/requirement" element={<ElevatorRequirement />} />
            <Route path="/requirement-pro" element={<ElevatorRequirementPro />} />
            <Route path="/maintenance" element={<MaintenanceService />} />
            <Route path="/complaint" element={<ComplaintChannel />} />
            <Route path="/contact" element={<Contact />} />
            <Route path="/elevator-drawings" element={<ElevatorDrawings />} />
            <Route path="/knowledge-hub" element={<KnowledgeHub />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App; 