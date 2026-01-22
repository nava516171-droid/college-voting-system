import React, { useState, useEffect } from "react";
import { api } from "../api";
import "../styles/LoginPage.css";

function LoginPage({ onLoginSuccess, onSwitchToRegister, onSwitchToAdminLogin, onSwitchToCandidateLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Check for login token in URL
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get("token");
    
    if (token) {
      loginWithToken(token);
    }
  }, []);

  const loginWithToken = async (token) => {
    setLoading(true);
    setError("");
    
    try {
      const response = await api.loginWithToken(token);
      if (response.access_token) {
        onLoginSuccess(response.access_token, response.user.email);
      } else {
        setError(response.detail || "Login failed");
      }
    } catch (err) {
      setError(err.message || "Invalid or expired login link");
    }
    setLoading(false);
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await api.login(email, password);
      if (response.access_token) {
        onLoginSuccess(response.access_token, email);
      } else {
        setError(response.detail || "Login failed");
      }
    } catch (err) {
      setError("Connection error. Is the server running?");
    }
    setLoading(false);
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h1>College Voting System</h1>
        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error && <div className="error">{error}</div>}
          <button type="submit" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        <div className="register-link">
          Don't have an account?{" "}
          <button className="link-button" onClick={onSwitchToRegister}>
            Register here
          </button>
        </div>

        <div className="register-link">
          Are you an admin?{" "}
          <button className="link-button" onClick={onSwitchToAdminLogin}>
            Admin Login
          </button>
        </div>

        <div className="register-link">
          Are you a candidate?{" "}
          <button className="link-button" onClick={onSwitchToCandidateLogin}>
            Candidate Login
          </button>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
