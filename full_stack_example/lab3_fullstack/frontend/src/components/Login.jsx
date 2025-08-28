import React from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

export default function Login() {
  const navigate = useNavigate();

  const handleBack = () => {
    navigate("/");
  };

  const handleGoogleLogin = () => {
    // Redirect to backend OAuth endpoint
    window.location.href = "http://localhost:8000/login";
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission logic here
    console.log("Login form submitted");
  };

  return (
    <div className="login-page">
      <button className="back-btn" onClick={handleBack}>
        &#8592; Back
      </button>
      <div className="login-container">
        <h2>Login to SoundPath</h2>
        <button className="google-btn" onClick={handleGoogleLogin}>
          <img 
            src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" 
            alt="Google logo" 
          />
          Login with Google
        </button>
        <div className="divider">or</div>
        <form onSubmit={handleSubmit}>
          <input 
            type="email" 
            name="email" 
            placeholder="Email" 
            required 
            autoComplete="username" 
          />
          <input 
            type="password" 
            name="password" 
            placeholder="Password" 
            required 
            autoComplete="current-password" 
          />
          <button type="submit">Login</button>
        </form>
        <div className="signup-link">
          Don't have an account? <a href="/register">Sign up</a>
        </div>
      </div>
    </div>
  );
}
