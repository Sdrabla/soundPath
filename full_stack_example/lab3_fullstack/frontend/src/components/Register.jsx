import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

export default function Register() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: ""
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleBack = () => {
    navigate("/");
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    // Validate passwords match
    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    // Validate password length
    if (formData.password.length < 6) {
      setError("Password must be at least 6 characters long");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/api/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: formData.name,
          email: formData.email,
          password: formData.password
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Registration failed");
      }

      // Registration successful, redirect to login
      navigate("/login", { state: { message: "Registration successful! Please log in." } });

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <button className="back-btn" onClick={handleBack}>
        &#8592; Back
      </button>
      <div className="login-container">
        <h2>Create Account</h2>
        <form onSubmit={handleSubmit}>
          <input 
            type="text" 
            name="name" 
            placeholder="Full Name" 
            required 
            autoComplete="name"
            value={formData.name}
            onChange={handleInputChange}
          />
          <input 
            type="email" 
            name="email" 
            placeholder="Email" 
            required 
            autoComplete="email"
            value={formData.email}
            onChange={handleInputChange}
          />
          <input 
            type="password" 
            name="password" 
            placeholder="Password" 
            required 
            autoComplete="new-password"
            value={formData.password}
            onChange={handleInputChange}
          />
          <input 
            type="password" 
            name="confirmPassword" 
            placeholder="Confirm Password" 
            required 
            autoComplete="new-password"
            value={formData.confirmPassword}
            onChange={handleInputChange}
          />
          <button type="submit" disabled={loading}>
            {loading ? "Creating Account..." : "Sign Up"}
          </button>
          {error && <div className="error-message">{error}</div>}
        </form>
        <div className="signup-link">
          Already have an account? <button onClick={() => navigate("/login")} style={{ background: "none", border: "none", color: "#007bff", cursor: "pointer", textDecoration: "underline", padding: 0, font: "inherit" }}>Log in</button>
        </div>
      </div>
    </div>
  );
}
