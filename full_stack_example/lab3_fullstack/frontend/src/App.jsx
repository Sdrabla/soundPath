import React, { useState, useEffect } from "react";
import { Routes, Route, useNavigate, useLocation } from "react-router-dom";
import "./App.css";
import Login from "./components/Login.jsx";
import Register from "./components/Register.jsx";
import Dashboard from "./components/Dashboard.jsx";
import Questionnaire from "./components/Questionnaire.jsx";

function LandingPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [userEmail, setUserEmail] = useState("");
  // Removed authError state - no longer needed

  useEffect(() => {
    // Check for OAuth callback parameters
    const urlParams = new URLSearchParams(location.search);
    const user = urlParams.get('user');
    const error = urlParams.get('error');
    
    if (user) {
      console.log('Setting user email and redirecting to dashboard...');
      setUserEmail(user);
      // Clear the URL parameters
      window.history.replaceState({}, document.title, window.location.pathname);
      // Redirect to dashboard with user email
      setTimeout(() => {
        console.log('Navigating to dashboard with user:', user);
        navigate("/dashboard", { state: { userEmail: user } });
      }, 2000);
    }
    
    // Removed error handling - let Google show its own error pages
  }, [location, navigate]);

  const handleGetStarted = () => {
    navigate("/login");
  };

  return (
    <div className="landing-page">
      <h1>soundPath</h1>
      <h3>Find the right gear for your sound</h3>
      
      {userEmail ? (
        <div className="user-welcome">
          <p>Welcome back, {userEmail}!</p>
          <p>Redirecting to dashboard...</p>
        </div>
      ) : (
        <>
          <p>Find personalized equipment, starter kits, and join communities all in one place! </p>
          <p>Sign up today and start your musical journey</p>
          <button id="signup-button" onClick={handleGetStarted}>
            Get Started
          </button>
          <button 
            onClick={() => navigate("/questionnaire")} 
            style={{
              background: "#4ea1ff",
              color: "white",
              border: "none",
              padding: "0.75rem 1.5rem",
              borderRadius: "4px",
              marginLeft: "1rem",
              cursor: "pointer",
              fontSize: "1rem"
            }}
          >
            Test Questionnaire
          </button>
        </>
      )}
      
      {/* Removed error display - Google will show its own error pages */}
      
      <img src="/vinyl-img.svg" alt="vinyl record" id="vinyl-img" />
      
      <div id="info-section">
        <h2> Why choose soundPath?</h2>
        <div className="info-item">
          <h3>Personalized Equipment Recommendations</h3>
          <p>You tell us how advanced you are and what your 
              looking for and well give you a personalized list 
              of what we think you'll love!</p>
        </div>
        <div className="info-item">
          <h3>Starter Kits</h3>
          <p>Just starting out? No biggie! Well give you 
              a step-by-step checklist of the essentials you 
              need to thrive!</p>
        </div>
        <div className="info-item">
          <h3>Unbiased Rankings</h3>
          <p>Unlike generic review sites, we provide 
              upgrade guidance, education and community. This 
              allows you to spend less time researching and more time 
              doing what you love!</p>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/questionnaire" element={<Questionnaire />} />
    </Routes>
  );
}
