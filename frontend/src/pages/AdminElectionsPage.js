import React, { useState, useEffect } from "react";
import { api } from "../api";
import "../styles/AdminElectionsPage.css";

function AdminElectionsPage() {
  const [elections, setElections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    description: "",
  });
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState("");

  useEffect(() => {
    fetchElections();
  }, []);

  const fetchElections = async () => {
    try {
      setLoading(true);
      const response = await api.getElections();
      setElections(Array.isArray(response) ? response : []);
      setError("");
    } catch (err) {
      console.error("Error fetching elections:", err);
      setError("Failed to load elections");
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError("");
    setSuccess("");

    if (!formData.name.trim()) {
      setError("Election name is required");
      setSubmitting(false);
      return;
    }

    try {
      const token = localStorage.getItem("adminToken");
      const apiUrl = window.location.hostname === 'localhost' 
        ? 'http://localhost:8001'
        : `http://${window.location.hostname}:8001`;

      const response = await fetch(`${apiUrl}/api/admin/elections`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Failed to create election");
      } else {
        setSuccess(`Election "${formData.name}" created successfully!`);
        setFormData({ name: "", description: "" });
        setShowForm(false);
        fetchElections();
        setTimeout(() => setSuccess(""), 3000);
      }
    } catch (err) {
      setError(err.message || "Error creating election");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <div className="elections-container">Loading elections...</div>;
  }

  return (
    <div className="elections-container">
      <div className="elections-header">
        <h1>📋 Elections Management</h1>
        <p>Manage all elections in the system</p>
        <button 
          className="create-btn" 
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? "✕ Cancel" : "➕ Create Election"}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      {showForm && (
        <div className="create-election-card">
          <h2>Create New Election</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="name">
                Election Name <span className="required">*</span>
              </label>
              <input
                id="name"
                type="text"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                placeholder="Enter election name"
                required
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label htmlFor="description">Description</label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                placeholder="Enter election description"
                className="form-input"
                rows="4"
              />
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="submit-btn"
            >
              {submitting ? "Creating..." : "Create Election"}
            </button>
          </form>
        </div>
      )}

      <div className="elections-grid">
        {elections.length === 0 ? (
          <div className="no-elections">
            <p>📭 No elections found</p>
            <p>Create one to get started!</p>
          </div>
        ) : (
          elections.map((election) => (
            <div key={election.id} className="election-card">
              <div className="election-card-header">
                <h3>{election.name || election.title}</h3>
                <span className="election-id">ID: {election.id}</span>
              </div>
              <p className="election-description">
                {election.description || "No description provided"}
              </p>
              <div className="election-footer">
                <button className="btn-edit">✏️ Edit</button>
                <button className="btn-delete">🗑️ Delete</button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default AdminElectionsPage;
