import React, { useState } from "react";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import FaceCapturePage from "./pages/FaceCapturePage";
import FaceDebugPage from "./pages/FaceDebugPage";
import OTPPage from "./pages/OTPPage";
import VotingPage from "./pages/VotingPage";
import ResultsPage from "./pages/ResultsPage";
import CandidatesCampaigningPage from "./pages/CandidatesCampaigningPage";
import CandidateLoginPage from "./pages/CandidateLoginPage";
import CandidateDashboardPage from "./pages/CandidateDashboardPage";
import AdminLoginPage from "./pages/AdminLoginPage";
import AdminRegisterPage from "./pages/AdminRegisterPage";
import AdminDashboardPage from "./pages/AdminDashboardPage";
import "./App.css";

function App() {
  const [currentPage, setCurrentPage] = useState("login");
  const [token, setToken] = useState(null);
  const [userEmail, setUserEmail] = useState(null);
  const [adminToken, setAdminToken] = useState(null);
  const [adminEmail, setAdminEmail] = useState(null);
  const [candidateToken, setCandidateToken] = useState(null);
  const [candidateId, setCandidateId] = useState(null);
  const [candidateName, setCandidateName] = useState(null);
  const [electionId] = useState(1);
  const [showResultsMessage, setShowResultsMessage] = useState(false);

  const handleLoginSuccess = (newToken, email) => {
    setToken(newToken);
    setUserEmail(email);
    localStorage.setItem("userEmail", email);
    // Go to face capture page after login
    setCurrentPage("face-capture");
  };

  const handleRegisterSuccess = () => {
    setCurrentPage("login");
  };

  const handleFaceSuccess = () => {
    setCurrentPage("home");
  };

  const handleOTPSuccess = () => {
    setCurrentPage("voting");
  };

  const handleVoteSuccess = () => {
    setCurrentPage("results");
  };

  const handleBackFromVoting = () => {
    setCurrentPage("login");
  };

  const handleBackFromResults = () => {
    setCurrentPage("home");
  };

  const handleBackToCampaigning = () => {
    setCurrentPage("home");
  };

  const handleViewResultsClick = () => {
    setShowResultsMessage(true);
    setTimeout(() => {
      setShowResultsMessage(false);
      setCurrentPage("results");
    }, 2000);
  };

  const handleAdminLoginSuccess = (newToken, email) => {
    setAdminToken(newToken);
    setAdminEmail(email);
    setCurrentPage("admin-dashboard");
  };

  const handleAdminRegisterSuccess = () => {
    setCurrentPage("admin-login");
  };

  const handleCandidateLoginSuccess = (newToken, newCandidateId, newCandidateName) => {
    setCandidateToken(newToken);
    setCandidateId(newCandidateId);
    setCandidateName(newCandidateName);
    setCurrentPage("candidate-dashboard");
  };

  const handleLogout = () => {
    setToken(null);
    setUserEmail(null);
    localStorage.removeItem("userEmail");
    setCurrentPage("login");
  };

  const handleCandidateLogout = () => {
    setCandidateToken(null);
    setCandidateId(null);
    setCandidateName(null);
    setCurrentPage("candidate-login");
  };
  const handleAdminLogout = () => {
    setAdminToken(null);
    setAdminEmail(null);
    localStorage.removeItem("adminToken");
    localStorage.removeItem("adminEmail");
    setCurrentPage("login");
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🗳️ College Voting System</h1>
        {token && (
          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        )}
        {adminToken && (
          <button className="logout-btn" onClick={handleAdminLogout}>
            Admin Logout
          </button>
        )}
        {candidateToken && (
          <button className="logout-btn" onClick={handleCandidateLogout}>
            Candidate Logout
          </button>
        )}
      </header>

      {showResultsMessage && (
        <div className="results-message-overlay">
          <div className="results-message-modal">
            <div className="message-icon">📊</div>
            <h2>Results Coming Soon</h2>
            <p>On the result date, the result will be displayed</p>
            <div className="loading-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      )}

      <main className="app-main">
        {currentPage === "home" && token && (
          <div className="home-page">
            <div className="home-container">
              <h1>Welcome to Voting Portal</h1>
              <div className="home-buttons">
                <button 
                  className="home-btn candidates-btn"
                  onClick={() => setCurrentPage("campaigning")}
                >
                  📢 Candidates Campaigning
                </button>
                <button 
                  className="home-btn voting-btn"
                  onClick={() => setCurrentPage("voting")}
                >
                  🗳️ Cast Your Vote
                </button>
                <button 
                  className="home-btn results-btn"
                  onClick={handleViewResultsClick}
                >
                  📊 View Results
                </button>
              </div>
            </div>
          </div>
        )}
        {currentPage === "login" && (
          <LoginPage
            onLoginSuccess={handleLoginSuccess}
            onSwitchToRegister={() => setCurrentPage("register")}
            onSwitchToAdminLogin={() => setCurrentPage("admin-login")}
            onSwitchToCandidateLogin={() => setCurrentPage("candidate-login")}
          />
        )}
        {currentPage === "register" && (
          <RegisterPage
            onRegisterSuccess={handleRegisterSuccess}
            onSwitchToLogin={() => setCurrentPage("login")}
          />
        )}
        {currentPage === "admin-login" && (
          <AdminLoginPage
            onAdminLoginSuccess={handleAdminLoginSuccess}
            onSwitchToUserLogin={() => setCurrentPage("login")}
            onSwitchToAdminRegister={() => setCurrentPage("admin-register")}
          />
        )}
        {currentPage === "admin-register" && (
          <AdminRegisterPage
            onAdminRegisterSuccess={handleAdminRegisterSuccess}
            onSwitchToAdminLogin={() => setCurrentPage("admin-login")}
          />
        )}
        {currentPage === "candidate-login" && (
          <CandidateLoginPage
            onLoginSuccess={handleCandidateLoginSuccess}
            onSwitchToUserLogin={() => setCurrentPage("login")}
          />
        )}
        {currentPage === "candidate-dashboard" && candidateToken && (
          <CandidateDashboardPage
            candidateToken={candidateToken}
            candidateId={candidateId}
            candidateName={candidateName}
            onLogout={handleCandidateLogout}
          />
        )}
        {currentPage === "admin-dashboard" && adminEmail && (
          <AdminDashboardPage
            adminEmail={adminEmail}
            onAdminLogout={handleAdminLogout}
          />
        )}
        {currentPage === "face-capture" && token && (
          <FaceCapturePage
            onFaceSuccess={handleFaceSuccess}
            token={token}
            userEmail={userEmail}
          />
        )}
        {currentPage === "debug" && (
          <FaceDebugPage />
        )}
        {currentPage === "otp" && (
          <OTPPage onOTPSuccess={handleOTPSuccess} token={token} userEmail={userEmail} />
        )}
        {currentPage === "voting" && token && (
          <VotingPage
            token={token}
            electionId={electionId}
            onVoteSuccess={handleVoteSuccess}
            onBackClick={handleBackFromVoting}
          />
        )}
        {currentPage === "campaigning" && token && (
          <CandidatesCampaigningPage
            token={token}
            electionId={electionId}
            onBackClick={handleBackToCampaigning}
          />
        )}
        {currentPage === "results" && <ResultsPage electionId={electionId} onBackClick={handleBackFromResults} />}
      </main>

      <footer className="app-footer">
        <p>© 2025 College Voting System. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
