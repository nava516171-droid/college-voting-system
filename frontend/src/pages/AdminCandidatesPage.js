import React, { useState, useEffect } from "react";
import { api } from "../api";
import "../styles/AdminCandidatesPage.css";

function AdminCandidatesPage({ onLogout }) {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchCandidates();
  }, []);

  const fetchCandidates = async () => {
    try {
      console.log("Fetching candidates...");
      
      const response = await api.getAllCandidates();
      
      console.log("Response received:", response);
      
      // Handle error response from API
      if (response && response.detail) {
        setError(`Server Error: ${response.detail}`);
        setCandidates([]);
      } else if (Array.isArray(response) && response.length >= 0) {
        console.log("Candidates loaded:", response.length);
        setCandidates(response);
        setError("");
      } else {
        setError(`Unexpected response format. Got: ${typeof response}`);
        setCandidates([]);
      }
    } catch (err) {
      console.error("Error fetching candidates:", err);
      const errorMessage = err instanceof Error ? err.message : String(err);
      setError(errorMessage || "Failed to load candidates from server");
      setCandidates([]);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="candidates-page-container">Loading candidates...</div>;
  }

  return (
    <div className="candidates-page-container">
      <div className="candidates-header">
        <h2>All Candidates</h2>
        <p className="candidates-count">Total: {candidates.length} candidates</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      {candidates.length === 0 ? (
        <div className="no-candidates">
          <p>No candidates found in the database</p>
        </div>
      ) : (
        <div className="candidates-table-wrapper">
          <table className="candidates-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Symbol Number</th>
                <th>Election ID</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {candidates.map((candidate) => (
                <tr key={candidate.id}>
                  <td className="cell-id">{candidate.id}</td>
                  <td className="cell-name">
                    <strong>{candidate.name}</strong>
                  </td>
                  <td className="cell-symbol">{candidate.symbol_number}</td>
                  <td className="cell-election">{candidate.election_id}</td>
                  <td className="cell-description">{candidate.description || "N/A"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default AdminCandidatesPage;
