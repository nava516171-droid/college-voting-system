import React, { useState, useEffect } from "react";
import { api } from "../api";
import AdminCandidatesPage from "./AdminCandidatesPage";
import AdminAddCandidatePage from "./AdminAddCandidatePage";
import AdminElectionsPage from "./AdminElectionsPage";
import AdminUsersPage from "./AdminUsersPage";
import AdminResultsPage from "./AdminResultsPage";
import "../styles/AdminDashboardPage.css";

function AdminDashboardPage({ adminEmail, onAdminLogout }) {
  const [adminProfile, setAdminProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeMenu, setActiveMenu] = useState("dashboard");
  const [statistics, setStatistics] = useState({
    totalUsers: 0,
    totalElections: 0,
    totalCandidates: 0,
    totalVotes: 0,
  });

  useEffect(() => {
    const fetchAdminProfile = async () => {
      try {
        const token = localStorage.getItem("adminToken");
        if (token) {
          const profile = await api.getAdminProfile(token);
          setAdminProfile(profile);
          
          // Fetch dashboard statistics from backend
          const stats = await api.getAdminStatistics(token);
          setStatistics({
            totalUsers: stats.total_users || 0,
            totalElections: stats.total_elections || 0,
            totalCandidates: stats.total_candidates || 0,
            totalVotes: stats.total_votes || 0,
          });
        }
      } catch (err) {
        console.error("Error fetching admin data:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchAdminProfile();
  }, []);

  if (loading) {
    return <div className="admin-dashboard-container">Loading...</div>;
  }

  const getInitials = (name) => {
    return name
      ?.split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase() || "A";
  };

  return (
    <div className="admin-dashboard-wrapper">
      {/* Sidebar */}
      <aside className="admin-sidebar">
        <div className="sidebar-header">
          <div className="admin-avatar">{getInitials(adminProfile?.full_name)}</div>
          <div className="admin-sidebar-info">
            <h4>{adminProfile?.full_name || "Admin"}</h4>
            <p>{adminProfile?.email}</p>
          </div>
        </div>

        <nav className="sidebar-nav">
          <div
            className={`nav-item ${activeMenu === "dashboard" ? "active" : ""}`}
            onClick={() => setActiveMenu("dashboard")}
          >
            <span className="nav-icon">📊</span>
            <span>Dashboard</span>
          </div>
          <div
            className={`nav-item ${activeMenu === "elections" ? "active" : ""}`}
            onClick={() => setActiveMenu("elections")}
          >
            <span className="nav-icon">🗳️</span>
            <span>Elections</span>
          </div>
          <div
            className={`nav-item ${activeMenu === "candidates" ? "active" : ""}`}
            onClick={() => setActiveMenu("candidates")}
          >
            <span className="nav-icon">👥</span>
            <span>View Candidates</span>
          </div>
          <div
            className={`nav-item ${activeMenu === "add-candidate" ? "active" : ""}`}
            onClick={() => setActiveMenu("add-candidate")}
          >
            <span className="nav-icon">➕</span>
            <span>Add Candidate</span>
          </div>
          <div
            className={`nav-item ${activeMenu === "users" ? "active" : ""}`}
            onClick={() => setActiveMenu("users")}
          >
            <span className="nav-icon">👤</span>
            <span>Users</span>
          </div>
          <div
            className={`nav-item ${activeMenu === "results" ? "active" : ""}`}
            onClick={() => setActiveMenu("results")}
          >
            <span className="nav-icon">📈</span>
            <span>Results</span>
          </div>
          <div
            className={`nav-item ${activeMenu === "settings" ? "active" : ""}`}
            onClick={() => setActiveMenu("settings")}
          >
            <span className="nav-icon">⚙️</span>
            <span>Settings</span>
          </div>
        </nav>

        <div className="sidebar-footer">
          <button className="logout-btn-sidebar" onClick={onAdminLogout}>
            🚪 Logout
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="admin-main-content">
        {activeMenu === "dashboard" && (
          <>
            <div className="admin-header">
              <div className="header-left">
                <h1>Dashboard</h1>
                <p>Welcome back, {adminProfile?.full_name || "Admin"}!</p>
              </div>
              <div className="header-right">
                <input type="text" className="search-box" placeholder="Search here..." />
                <button className="report-btn">📊 Generate Report</button>
              </div>
            </div>

            {/* Statistics Cards */}
            <div className="stats-grid">
              <div className="stat-card" onClick={() => setActiveMenu("candidates")}>
                <div className="stat-icon icon-blue">👥</div>
                <div className="stat-content">
                  <h3>{statistics.totalUsers}</h3>
                  <p>Total Users</p>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon icon-purple">🗳️</div>
                <div className="stat-content">
                  <h3>{statistics.totalElections}</h3>
                  <p>Total Elections</p>
                </div>
              </div>

              <div className="stat-card" onClick={() => setActiveMenu("candidates")} style={{cursor: "pointer"}}>
                <div className="stat-icon icon-pink">🎯</div>
                <div className="stat-content">
                  <h3>{statistics.totalCandidates}</h3>
                  <p>Total Candidates</p>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon icon-cyan">✅</div>
                <div className="stat-content">
                  <h3>{statistics.totalVotes}</h3>
                  <p>Total Votes Cast</p>
                </div>
          </div>
        </div>

        {/* Charts Section */}
        <div className="charts-section">
          <div className="chart-container">
            <h3>Voting Overview</h3>
            <div className="pie-chart-wrapper">
              <div className="pie-chart-placeholder">
                <div className="simple-pie-chart">
                  <div className="pie-segment" style={{ "--color": "#667eea" }}></div>
                  <div className="pie-segment" style={{ "--color": "#764ba2" }}></div>
                  <div className="pie-segment" style={{ "--color": "#f093fb" }}></div>
                  <div className="pie-segment" style={{ "--color": "#4facfe" }}></div>
                </div>
              </div>
              <div className="legend">
                <div className="legend-item">
                  <span className="legend-color" style={{ backgroundColor: "#667eea" }}></span>
                  <span>Dinesh Rangappa (30%)</span>
                </div>
                <div className="legend-item">
                  <span className="legend-color" style={{ backgroundColor: "#764ba2" }}></span>
                  <span>Ramesh (25%)</span>
                </div>
                <div className="legend-item">
                  <span className="legend-color" style={{ backgroundColor: "#f093fb" }}></span>
                  <span>Nirmala Hiremani (25%)</span>
                </div>
                <div className="legend-item">
                  <span className="legend-color" style={{ backgroundColor: "#4facfe" }}></span>
                  <span>Others (20%)</span>
                </div>
              </div>
            </div>
          </div>

          <div className="info-container">
            <div className="wallet-card">
              <div className="wallet-info">
                <h4>Election Status</h4>
                <p className="wallet-amount">{statistics.totalVotes} Votes</p>
                <p className="wallet-subtext">+15% from last week</p>
              </div>
              <div className="wallet-icon">💰</div>
            </div>

            <div className="activity-section">
              <h3>Recent Activity</h3>
              <div className="activity-list">
                <div className="activity-item">
                  <span className="activity-icon">🗳️</span>
                  <div className="activity-content">
                    <p>New vote received</p>
                    <small>2 minutes ago</small>
                  </div>
                </div>
                <div className="activity-item">
                  <span className="activity-icon">👤</span>
                  <div className="activity-content">
                    <p>New user registered</p>
                    <small>15 minutes ago</small>
                  </div>
                </div>
                <div className="activity-item">
                  <span className="activity-icon">✅</span>
                  <div className="activity-content">
                    <p>Vote verified</p>
                    <small>1 hour ago</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="quick-actions">
          <div className="action-card">
            <h4> Reports</h4>
            <p>Generate reports</p>
            <button>Generate</button>
          </div>
        </div>
          </>
        )}

        {activeMenu === "add-candidate" && <AdminAddCandidatePage />}
        {activeMenu === "elections" && <AdminElectionsPage />}
        {activeMenu === "candidates" && <AdminCandidatesPage onLogout={onAdminLogout} />}
        {activeMenu === "users" && <AdminUsersPage />}
        {activeMenu === "results" && <AdminResultsPage />}
      </main>
    </div>
  );
}

export default AdminDashboardPage;
