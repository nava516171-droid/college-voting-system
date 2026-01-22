import React, { useState, useEffect } from "react";
import { api } from "../api";
import "../styles/AdminUsersPage.css";

function AdminUsersPage() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedUser, setSelectedUser] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const token = localStorage.getItem("adminToken");
        if (token) {
          const usersData = await api.getUsers(token);
          setUsers(usersData);
          // Auto-select first user if available
          if (usersData.length > 0) {
            setSelectedUser(usersData[0]);
          }
        }
      } catch (err) {
        console.error("Error fetching users:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  if (loading) {
    return <div className="users-container">Loading users...</div>;
  }

  if (error) {
    return <div className="users-container error">{error}</div>;
  }

  return (
    <div className="users-page">
      {/* Users Sidebar List */}
      <div className="users-sidebar">
        <div className="users-header">
          <h2>Registered Users</h2>
          <span className="users-count">{users.length}</span>
        </div>
        <div className="users-list">
          {users.length === 0 ? (
            <p className="no-users">No users found</p>
          ) : (
            users.map((user) => (
              <div
                key={user.id}
                className={`user-item ${selectedUser?.id === user.id ? "active" : ""}`}
                onClick={() => setSelectedUser(user)}
              >
                <div className="user-avatar">
                  {user.full_name
                    ?.split(" ")
                    .map((n) => n[0])
                    .join("")
                    .toUpperCase() || "U"}
                </div>
                <div className="user-info">
                  <p className="user-name">{user.full_name}</p>
                  <p className="user-email">{user.email}</p>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* User Details Panel */}
      <div className="user-details-panel">
        {selectedUser ? (
          <div className="user-details">
            <div className="details-header">
              <div className="details-avatar">
                {selectedUser.full_name
                  ?.split(" ")
                  .map((n) => n[0])
                  .join("")
                  .toUpperCase() || "U"}
              </div>
              <div className="details-title">
                <h2>{selectedUser.full_name}</h2>
              </div>
            </div>

            <div className="details-content">
              <div className="detail-item">
                <label>Full Name</label>
                <p>{selectedUser.full_name}</p>
              </div>
              <div className="detail-item">
                <label>Email Address</label>
                <p>{selectedUser.email}</p>
              </div>
              <div className="detail-item">
                <label>Roll Number</label>
                <p>{selectedUser.roll_number || "N/A"}</p>
              </div>
              <div className="detail-item">
                <label>Registered Date</label>
                <p>
                  {selectedUser.created_at
                    ? new Date(selectedUser.created_at).toLocaleDateString()
                    : "N/A"}
                </p>
              </div>
            </div>

            <div className="user-actions">
              <button className="btn-action btn-message">📧 Send Message</button>
              <button className="btn-action btn-verify">✅ Verify User</button>
            </div>
          </div>
        ) : (
          <div className="no-selection">
            <p>Select a user to view details</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default AdminUsersPage;
