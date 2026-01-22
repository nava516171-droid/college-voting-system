import React, { useState } from "react";
import { api } from "../api";
import "../styles/CandidateLoginPage.css";

function CandidateLoginPage({ onLoginSuccess, onSwitchToUserLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await api.candidateLogin(email, password);
      if (response.access_token) {
        onLoginSuccess(response.access_token, response.candidate_id, response.candidate_name);
      } else {
        setError(response.detail || "Login failed");
      }
    } catch (err) {
      setError(err.message || "Connection error. Is the server running?");
    }
    setLoading(false);
  };

  return (
    <div className="candidate-login-container">
      <div className="candidate-login-box">
        <h1>📢 Candidate Portal</h1>
        <p className="subtitle">Login to manage your campaign</p>
        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              required
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
            />
          </div>

          {error && <div className="error">{error}</div>}

          <button type="submit" className="login-button" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        <div className="login-links">
          <p>
            <button className="link-button" onClick={onSwitchToUserLogin}>
              Back to User Login
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}

export default CandidateLoginPage;
