import React, { useState, useEffect } from "react";
import { api } from "../api";
import "../styles/ResultsPage.css";

function ResultsPage({ electionId, onBackClick }) {
  const [results, setResults] = useState([]);
  const [election, setElection] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchElectionAndResults();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [electionId]);

  const fetchElectionAndResults = async () => {
    try {
      // Fetch election details
      const electionsData = await api.getElections();
      const currentElection = electionsData.find(e => e.id === electionId);
      setElection(currentElection);

      // Fetch results
      const response = await api.getResults(electionId);
      setResults(Array.isArray(response) ? response : []);
    } catch (err) {
      setError("Failed to load results");
    }
    setLoading(false);
  };

  if (loading) return <div className="loading">Loading results...</div>;

  // Check if election is still open (not ended)
  const isElectionOpen = election && election.status && election.status.toLowerCase() !== 'ended';

  // If election is still open, show "Results Coming Soon"
  if (isElectionOpen) {
    return (
      <div className="results-container">
        <button className="back-button" onClick={onBackClick} title="Go Back">
          ←
        </button>
        <div className="results-header">
          <h1>Results Coming Soon</h1>
        </div>
        <div className="coming-soon-container">
          <div className="chart-icon">
            <div className="chart-bars">
              <div className="bar bar-1"></div>
              <div className="bar bar-2"></div>
              <div className="bar bar-3"></div>
            </div>
          </div>
          <p className="coming-soon-text">On the result date, the result will be displayed</p>
          <div className="loading-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    );
  }

  // If election has ended, show full results
  const totalVotes = results.reduce((sum, r) => sum + (r.vote_count || 0), 0);
  const winner = results.length > 0 ? results[0] : null;

  return (
    <div className="results-container">
      <button className="back-button" onClick={onBackClick} title="Go Back">
        ←
      </button>
      <div className="results-header">
        <h1>Election Results</h1>
      </div>
      {error && <div className="error">{error}</div>}

      {winner && (
        <div className="winner-box">
          <h2>🏆 Leading Candidate</h2>
          <h3>{winner.candidate_name}</h3>
          <p>{winner.vote_count} votes</p>
        </div>
      )}

      <div className="results-list">
        <h3>All Results</h3>
        {results.map((result, index) => (
          <div key={index} className="result-item">
            <span className="rank">{index + 1}.</span>
            <span className="name">{result.candidate_name}</span>
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{
                  width: totalVotes > 0 ? (result.vote_count / totalVotes) * 100 : 0,
                }}
              ></div>
            </div>
            <span className="votes">{result.vote_count} votes</span>
          </div>
        ))}
      </div>

      <div className="total-votes">Total Votes: {totalVotes}</div>
    </div>
  );
}

export default ResultsPage;
