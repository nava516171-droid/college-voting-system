import React, { useState, useEffect } from "react";
import { api } from "../api";
import "../styles/OTPPage.css";

function OTPPage({ token, onOTPSuccess, userEmail }) {
  const [otpCode, setOtpCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [otpRequested, setOtpRequested] = useState(false);
  const [countdown, setCountdown] = useState(0);

  // Request OTP on component mount
  useEffect(() => {
    requestOTP();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Countdown timer for resend button
  useEffect(() => {
    if (countdown <= 0) return;
    const timer = setTimeout(() => setCountdown(countdown - 1), 1000);
    return () => clearTimeout(timer);
  }, [countdown]);

  const requestOTP = async () => {
    setLoading(true);
    setError("");
    setSuccess("");

    try {
      const emailToUse = userEmail || localStorage.getItem("userEmail");
      console.log("Requesting OTP for email:", emailToUse);
      console.log("Token:", token ? token.substring(0, 20) + "..." : "No token");
      
      const response = await api.requestOTP(emailToUse, token);
      console.log("OTP Request Response:", response);
      
      if (response.message) {
        setSuccess(`✅ ${response.message} This email includes your welcome letter and OTP code.`);
        setOtpRequested(true);
        setCountdown(30); // 30 second cooldown before resend
      } else {
        setError("Failed to send OTP. Please try again.");
      }
    } catch (err) {
      console.error("OTP Request Error:", err);
      setError(err.message || "Error requesting OTP. Check your connection.");
    }
    setLoading(false);
  };

  const handleVerify = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await api.verifyOTP(otpCode, token);
      if (response.is_verified) {
        setSuccess("OTP verified successfully! Proceeding...");
        setTimeout(() => onOTPSuccess(), 1500);
      } else {
        setError("Invalid OTP. Please try again.");
      }
    } catch (err) {
      setError(err.message || "Error verifying OTP");
    }
    setLoading(false);
  };

  return (
    <div className="otp-container">
      <div className="otp-box">
        <h1>Verify OTP</h1>
        <p>Enter the OTP sent to your email</p>
        
        {!otpRequested && (
          <div className="request-section">
            <p className="subtitle">No OTP yet?</p>
            <button 
              type="button"
              onClick={requestOTP} 
              disabled={loading}
              className="request-button"
            >
              {loading ? "Sending..." : "Send OTP to Email"}
            </button>
          </div>
        )}

        {otpRequested && (
          <form onSubmit={handleVerify}>
            <div className="form-group">
              <label>OTP Code</label>
              <input
                type="text"
                value={otpCode}
                onChange={(e) => setOtpCode(e.target.value.replace(/[^0-9]/g, "").slice(0, 6))}
                maxLength="6"
                placeholder="000000"
                required
              />
              <p className="help-text">Check your email for the 6-digit code</p>
            </div>

            {error && <div className="error">{error}</div>}
            {success && <div className="success">{success}</div>}

            <button type="submit" disabled={loading || otpCode.length !== 6}>
              {loading ? "Verifying..." : "Verify OTP"}
            </button>

            <div className="resend-section">
              <p className="resend-text">Didn't receive the code?</p>
              <button
                type="button"
                onClick={requestOTP}
                disabled={countdown > 0 || loading}
                className="resend-button"
              >
                {countdown > 0 ? `Resend in ${countdown}s` : "Resend OTP"}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}

export default OTPPage;
