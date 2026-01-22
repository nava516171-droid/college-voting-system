import React, { useState } from "react";
import { api } from "../api";
import "../styles/AdminLoginPage.css";

function AdminLoginPage({ onAdminLoginSuccess, onSwitchToUserLogin, onSwitchToAdminRegister }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await api.adminLogin(email, password);
      
      if (response.access_token) {
        localStorage.setItem("adminToken", response.access_token);
        localStorage.setItem("adminEmail", email);
        onAdminLoginSuccess(response.access_token, email);
      } else {
        setError("Login failed. Please try again.");
      }
    } catch (err) {
      setError(err.message || "Invalid email or password");
    }
    setLoading(false);
  };

  return (
    <div className="admin-login-container">
      <div className="admin-login-box">
        <h1>🔐 Admin Login</h1>
        <p>Access the admin dashboard</p>

        {error && <div className="error">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="admin@example.com"
              required
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>

          <button type="submit" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        <div className="auth-links">
          <p>
            Don't have an admin account?{" "}
            <button type="button" className="link-button" onClick={onSwitchToAdminRegister}>
              Register here
            </button>
          </p>
          <p>
            User login?{" "}
            <button type="button" className="link-button" onClick={onSwitchToUserLogin}>
              Switch to User Login
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}

export default AdminLoginPage;
