import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Questionnaire.css";

export default function Questionnaire() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    experience: "",
    instrument: "",
    goal: "",
    genre: "",
    budget: ""
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission - you can add API call here later
    console.log("Questionnaire submitted:", formData);
    // For now, just redirect to dashboard
    navigate("/dashboard");
  };

  const handleBack = () => {
    navigate("/dashboard");
  };

  return (
    <div className="questionnaire-page">
      <header className="questionnaire-header">
        <button onClick={handleBack} className="back-btn">
          &#8592; Back to Dashboard
        </button>
        <h1>soundPath</h1>
      </header>

      <div className="container">
        <h2>Tell us about your musical journey 🎶</h2>
        <form onSubmit={handleSubmit}>
          <label htmlFor="experience">How would you describe your experience level?</label>
          <select 
            id="experience" 
            name="experience" 
            value={formData.experience}
            onChange={handleInputChange}
            required
          >
            <option value="">-- Select --</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>

          <label htmlFor="instrument">What instrument are you most interested in?</label>
          <input 
            type="text" 
            id="instrument" 
            name="instrument" 
            placeholder="e.g., Guitar, Piano, Drums" 
            value={formData.instrument}
            onChange={handleInputChange}
            required 
          />

          <label htmlFor="goal">What's your main goal with music?</label>
          <textarea 
            id="goal" 
            name="goal" 
            rows="3" 
            placeholder="e.g., Start a band, play casually, improve skills" 
            value={formData.goal}
            onChange={handleInputChange}
            required 
          />

          <label htmlFor="genre">Which genres do you enjoy?</label>
          <select 
            id="genre" 
            name="genre" 
            value={formData.genre}
            onChange={handleInputChange}
            required
          >
            <option value="">-- Select --</option>
            <option value="jazz">Jazz</option>
            <option value="pop">Pop</option>
            <option value="hiphop">Hip Hop</option>
            <option value="rock">Rock</option>
            <option value="classical">Classical</option>
            <option value="electronic">Electronic</option>
            <option value="country">Country</option>
            <option value="blues">Blues</option>
            <option value="folk">Folk</option>
            <option value="other">Other</option>
          </select>

          <label htmlFor="budget">What's your budget range?</label>
          <select 
            id="budget" 
            name="budget" 
            value={formData.budget}
            onChange={handleInputChange}
            required
          >
            <option value="">-- Select --</option>
            <option value="under-100">Under $100</option>
            <option value="100-300">$100 - $300</option>
            <option value="300-500">$300 - $500</option>
            <option value="500-1000">$500 - $1000</option>
            <option value="over-1000">Over $1000</option>
          </select>

          <button type="submit">Get My Recommendations! 🎸</button>
        </form>
      </div>
    </div>
  );
}
