import React, { useState, useEffect } from "react";
import { api } from "../api";
import "../styles/AdminAddCandidatePage.css";

function AdminAddCandidatePage() {
  const [elections, setElections] = useState([]);
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [showElectionForm, setShowElectionForm] = useState(false);

  const [formData, setFormData] = useState({
    election_id: "",
    name: "",
    symbol_number: "",
    description: "",
  });

  const [electionFormData, setElectionFormData] = useState({
    name: "",
    description: "",
  });

  useEffect(() => {
    console.log("AdminAddCandidatePage mounted");
    fetchElections();
  }, []);

  useEffect(() => {
    console.log("formData.election_id changed:", formData.election_id);
    if (formData.election_id) {
      fetchCandidatesForElection(formData.election_id);
    } else {
      setCandidates([]);
    }
  }, [formData.election_id]);

  const fetchElections = async () => {
    try {
      console.log("Fetching elections...");
      const response = await api.getElections();
      console.log("Elections fetched:", response);
      setElections(Array.isArray(response) ? response : []);
      setLoading(false);
    } catch (err) {
      console.error("Error fetching elections:", err);
      setError("Failed to load elections");
      setLoading(false);
    }
  };

  const fetchCandidatesForElection = async (electionId) => {
    try {
      console.log(`Fetching candidates for election ${electionId}...`);
      const response = await api.getCandidates(electionId);
      console.log("Candidates fetched:", response);
      setCandidates(Array.isArray(response) ? response : []);
    } catch (err) {
      console.error("Error fetching candidates:", err);
      setCandidates([]);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    const newValue = name === "election_id" || name === "symbol_number" ? parseInt(value) || "" : value;
    console.log(`Field change: ${name} = ${newValue}`);
    setFormData((prev) => ({
      ...prev,
      [name]: newValue,
    }));
  };

  const handleElectionFormChange = (e) => {
    const { name, value } = e.target;
    setElectionFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setSubmitting(true);

    if (!formData.election_id || !formData.name || !formData.symbol_number) {
      setError("Please fill in all required fields");
      setSubmitting(false);
      return;
    }

    try {
      const token = localStorage.getItem("adminToken");
      const apiUrl = window.location.hostname === 'localhost' 
        ? 'http://localhost:8001'
        : `http://${window.location.hostname}:8001`;
      
      const response = await fetch(`${apiUrl}/api/admin/candidates`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Failed to add candidate");
      } else {
        setSuccess(`Candidate '${formData.name}' added successfully!`);
        setFormData({
          election_id: formData.election_id,
          name: "",
          symbol_number: "",
          description: "",
        });
        // Refresh candidates list
        fetchCandidatesForElection(formData.election_id);
        setTimeout(() => setSuccess(""), 3000);
      }
    } catch (err) {
      setError(err.message || "Error adding candidate");
    }
    setSubmitting(false);
  };

  if (loading) {
    return <div className="add-candidate-container">Loading elections...</div>;
  }

  const selectedElection = elections.find(e => e.id === formData.election_id);

  return (
    <div className="add-candidate-container">
      <div className="add-candidate-grid">
        {/* Left Column: Elections List */}
        <div className="elections-card">
          <div className="card-header">
            <h3>📋 All Elections ({elections.length})</h3>
            <button 
              className="add-election-btn"
              onClick={() => setShowElectionForm(!showElectionForm)}
              title="Create new election"
            >
              {showElectionForm ? "✕" : "➕"}
            </button>
          </div>

          {showElectionForm && (
            <div className="election-form-section">
              <h4>Create New Election</h4>
              <form onSubmit={(e) => { 
                e.preventDefault(); 
                alert("Election creation feature coming soon!");
              }}>
                <div className="form-group-small">
                  <input
                    type="text"
                    name="name"
                    placeholder="Election name"
                    value={electionFormData.name}
                    onChange={handleElectionFormChange}
                    className="form-input-small"
                  />
                </div>
                <div className="form-group-small">
                  <textarea
                    name="description"
                    placeholder="Description"
                    value={electionFormData.description}
                    onChange={handleElectionFormChange}
                    className="form-input-small"
                    rows="2"
                  />
                </div>
                <button type="submit" className="submit-btn-small">Create</button>
              </form>
            </div>
          )}

          <div className="elections-list">
            {elections.length === 0 ? (
              <div className="no-items">
                <p>No elections found</p>
              </div>
            ) : (
              elections.map((election) => (
                <div 
                  key={election.id}
                  className={`election-item ${formData.election_id === election.id ? 'active' : ''}`}
                  onClick={() => setFormData({...formData, election_id: election.id})}
                >
                  <div className="election-item-header">
                    <strong>ID: {election.id}</strong>
                    <span className="election-name">{election.name}</span>
                  </div>
                  {election.description && (
                    <p className="election-desc">{election.description}</p>
                  )}
                </div>
              ))
            )}
          </div>
        </div>

        {/* Right Column: Add Candidate Form + Candidates List */}
        <div className="right-column">
          {/* Add Candidate Form */}
          <div className="add-candidate-card">
            <h2>➕ Add Candidate</h2>
            {selectedElection ? (
              <div className="selected-election-info">
                <p><strong>Selected Election:</strong> {selectedElection.name}</p>
                <p><strong>Election ID:</strong> {selectedElection.id}</p>
              </div>
            ) : (
              <p className="select-election-msg">👈 Select an election from the left</p>
            )}

            {error && <div className="error-message">{error}</div>}
            {success && <div className="success-message">{success}</div>}

            {selectedElection && (
              <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <label htmlFor="name">
                    Candidate Name <span className="required">*</span>
                  </label>
                  <input
                    id="name"
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="Enter candidate full name"
                    required
                    className="form-input"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="symbol_number">
                    Symbol Number <span className="required">*</span>
                  </label>
                  <input
                    id="symbol_number"
                    type="number"
                    name="symbol_number"
                    value={formData.symbol_number}
                    onChange={handleChange}
                    placeholder="Enter symbol/ballot number"
                    required
                    className="form-input"
                    min="1"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="description">Description</label>
                  <textarea
                    id="description"
                    name="description"
                    value={formData.description}
                    onChange={handleChange}
                    placeholder="Enter candidate description"
                    className="form-input"
                    rows="3"
                  />
                </div>

                <button
                  type="submit"
                  disabled={submitting}
                  className="submit-btn"
                >
                  {submitting ? "Adding..." : "Add Candidate"}
                </button>
              </form>
            )}
          </div>

          {/* Candidates List */}
          {selectedElection && candidates.length > 0 && (
            <div className="candidates-list-card">
              <h3>📊 Candidates in {selectedElection.name}</h3>
              <p className="subtitle">Total: {candidates.length} candidates</p>

              <div className="candidates-table-wrapper">
                <table className="candidates-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Symbol</th>
                      <th>Description</th>
                    </tr>
                  </thead>
                  <tbody>
                    {candidates.map((candidate) => (
                      <tr key={candidate.id}>
                        <td className="cell-id">{candidate.id}</td>
                        <td className="cell-name">{candidate.name}</td>
                        <td className="cell-symbol">{candidate.symbol_number}</td>
                        <td className="cell-description">{candidate.description || "—"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default AdminAddCandidatePage;
