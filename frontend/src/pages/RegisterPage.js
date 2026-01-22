import React, { useState } from "react";
import { api } from "../api";
import "../styles/RegisterPage.css";

function RegisterPage({ onRegisterSuccess, onSwitchToLogin }) {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    confirmPassword: "",
    full_name: "",
    roll_number: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [registeredEmail, setRegisteredEmail] = useState("");
  const [registrationStep, setRegistrationStep] = useState("form"); // "form" or "otp-verify"
  const [otpCode, setOtpCode] = useState("");
  const [otpError, setOtpError] = useState("");
  const [otpLoading, setOtpLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    // Validation
    if (!formData.email || !formData.password || !formData.full_name || !formData.roll_number) {
      setError("All fields are required");
      setLoading(false);
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      setLoading(false);
      return;
    }

    if (formData.password.length < 6) {
      setError("Password must be at least 6 characters");
      setLoading(false);
      return;
    }

    try {
      const response = await api.register(
        formData.email,
        formData.password,
        formData.full_name,
        formData.roll_number
      );

      if (response.id || response.email) {
        setSuccess("✅ Account created successfully! OTP sent to your email...");
        setRegisteredEmail(formData.email);
        localStorage.setItem("registeredEmail", formData.email);
        
        // After 2 seconds, move to OTP verification
        setTimeout(() => {
          setRegistrationStep("otp-verify");
          setSuccess("");
        }, 2000);
      } else {
        setError(response.detail || "Registration failed");
      }
    } catch (err) {
      setError(err.message || "Connection error. Is the server running?");
    }
    setLoading(false);
  };

  const handleVerifyOTP = async (e) => {
    e.preventDefault();
    setOtpError("");
    setOtpLoading(true);

    if (!otpCode.trim()) {
      setOtpError("Please enter the OTP code");
      setOtpLoading(false);
      return;
    }

    try {
      // Create a temporary token for OTP verification
      const loginResponse = await api.login(registeredEmail, formData.password);
      const tempToken = loginResponse.access_token;

      const verifyResponse = await api.verifyOTP(otpCode, tempToken);
      
      if (verifyResponse.is_verified || verifyResponse.message) {
        setSuccess("✅ OTP verified! Account confirmed. Redirecting to login...");
        setTimeout(() => {
          localStorage.removeItem("registeredEmail");
          onRegisterSuccess();
        }, 2000);
      } else {
        setOtpError("Invalid OTP. Please try again.");
      }
    } catch (err) {
      setOtpError(err.message || "Error verifying OTP");
    }
    setOtpLoading(false);
  };

  return (
    <div className="register-container">
      <div className="register-box">
        {registrationStep === "form" ? (
          <>
            <h1>Create Account</h1>
            <p>Join the College Voting System</p>

            <form onSubmit={handleRegister}>
              <div className="form-group">
                <label>Full Name</label>
                <input
                  type="text"
                  name="full_name"
                  value={formData.full_name}
                  onChange={handleChange}
                  placeholder="Name"
                  required
                />
              </div>

              <div className="form-group">
                <label>Roll Number</label>
                <input
                  type="text"
                  name="roll_number"
                  value={formData.roll_number}
                  onChange={handleChange}
                  placeholder="2024001"
                  required
                />
              </div>

              <div className="form-group">
                <label>Email</label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="student@college.com"
                  required
                />
              </div>

              <div className="form-group">
                <label>Password</label>
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="At least 6 characters"
                  required
                />
              </div>

              <div className="form-group">
                <label>Confirm Password</label>
                <input
                  type="password"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  placeholder="Confirm your password"
                  required
                />
              </div>

              {error && <div className="error">{error}</div>}
              {success && <div className="success">{success}</div>}

              <button type="submit" disabled={loading}>
                {loading ? "Creating Account..." : "Register"}
              </button>
            </form>

            <div className="login-link">
              Already have an account?{" "}
              <button className="link-button" onClick={onSwitchToLogin}>
                Login here
              </button>
            </div>
          </>
        ) : (
          <>
            <h1>Verify Your Email</h1>
            <p>OTP sent to {registeredEmail}</p>

            <form onSubmit={handleVerifyOTP}>
              <div className="form-group">
                <label>Enter OTP Code</label>
                <input
                  type="text"
                  value={otpCode}
                  onChange={(e) => setOtpCode(e.target.value)}
                  placeholder="Enter 6-digit OTP"
                  maxLength="6"
                  required
                />
              </div>

              <div className="otp-info">
                <p>📧 Check your email for the OTP code</p>
                <p>The code is valid for 10 minutes</p>
              </div>

              {otpError && <div className="error">{otpError}</div>}
              {success && <div className="success">{success}</div>}

              <button type="submit" disabled={otpLoading}>
                {otpLoading ? "Verifying..." : "Verify OTP"}
              </button>
            </form>

            <div className="back-link">
              <button className="link-button" onClick={() => setRegistrationStep("form")}>
                ← Back to Registration
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default RegisterPage;
