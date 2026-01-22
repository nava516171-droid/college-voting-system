import React, { useState, useEffect } from "react";
import { api } from "../api";
import "../styles/AdminResultsPage.css";

function AdminResultsPage() {
  const [elections, setElections] = useState([]);
  const [selectedElectionId, setSelectedElectionId] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchElections = async () => {
      try {
        const electionsData = await api.getElections();
        setElections(Array.isArray(electionsData) ? electionsData : []);
        // Auto-select first election if available
        if (electionsData && electionsData.length > 0) {
          setSelectedElectionId(electionsData[0].id);
          fetchResults(electionsData[0].id);
        } else {
          setLoading(false);
        }
      } catch (err) {
        console.error("Error fetching elections:", err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchElections();
  }, []);

  const fetchResults = async (electionId) => {
    try {
      setLoading(true);
      const resultsData = await api.getResults(electionId);
      setResults(Array.isArray(resultsData) ? resultsData : []);
      setError(null);
    } catch (err) {
      console.error("Error fetching results:", err);
      setError(err.message);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleElectionChange = (electionId) => {
    setSelectedElectionId(electionId);
    fetchResults(electionId);
  };

  const totalVotes = results.reduce((sum, r) => sum + (r.vote_count || 0), 0);
  const winner = results.length > 0 ? results[0] : null;

  const selectedElection = elections.find((e) => e.id === selectedElectionId);

  return (
    <div className="admin-results-page">
      {/* Election Selector */}
      <div className="election-selector">
        <h2>Select Election</h2>
        {elections.length === 0 ? (
          <p className="no-elections">No elections found</p>
        ) : (
          <div className="election-buttons">
            {elections.map((election) => (
              <button
                key={election.id}
                className={`election-btn ${selectedElectionId === election.id ? "active" : ""}`}
                onClick={() => handleElectionChange(election.id)}
              >
                <span className="election-title">{election.title}</span>
                <span className="election-status">{election.status || "Active"}</span>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Results Display */}
      {loading ? (
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading results...</p>
        </div>
      ) : error ? (
        <div className="error-container">
          <p className="error-message">⚠️ {error}</p>
        </div>
      ) : results.length === 0 ? (
        <div className="no-results">
          <p>🗳️ No candidates found for {selectedElection?.title || "this election"}</p>
        </div>
      ) : (
        <div className="results-content">
          {/* Winner Box */}
          {winner && (
            <div className="winner-section">
              <div className="winner-card">
                <div className="trophy-icon">🏆</div>
                <h2>Leading Candidate</h2>
                <h3 className="winner-name">{winner.candidate_name}</h3>
                <p className="winner-votes">{winner.vote_count} votes</p>
              </div>
            </div>
          )}

          {/* Detailed Results */}
          <div className="detailed-results">
            <h2>Voting Results Breakdown</h2>
            <div className="results-grid">
              {results.map((result, index) => (
                <div key={index} className="result-card">
                  <div className="result-header">
                    <span className="rank">#{index + 1}</span>
                    <span className="candidate-name">{result.candidate_name}</span>
                  </div>
                  <div className="progress-section">
                    <div className="progress-bar">
                      <div
                        className="progress-fill"
                        style={{
                          width: totalVotes > 0 ? (result.vote_count / totalVotes) * 100 : 0,
                          backgroundColor:
                            index === 0
                              ? "#667eea"
                              : index === 1
                              ? "#764ba2"
                              : index === 2
                              ? "#f093fb"
                              : "#4facfe",
                        }}
                      ></div>
                    </div>
                    <div className="result-stats">
                      <span className="vote-count">{result.vote_count} votes</span>
                      <span className="vote-percentage">
                        {totalVotes > 0 ? ((result.vote_count / totalVotes) * 100).toFixed(1) : 0}%
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Summary Stats */}
          <div className="summary-stats">
            <div className="stat-box">
              <h4>Total Votes Cast</h4>
              <p className="stat-value">{totalVotes}</p>
            </div>
            <div className="stat-box">
              <h4>Total Candidates</h4>
              <p className="stat-value">{results.length}</p>
            </div>
            <div className="stat-box">
              <h4>Highest Votes</h4>
              <p className="stat-value">{winner?.vote_count || 0}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default AdminResultsPage;
