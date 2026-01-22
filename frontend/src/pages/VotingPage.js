import React, { useState, useEffect, useCallback } from "react";
import { api } from "../api";
import "../styles/VotingPage.css";

function VotingPage({ token, electionId, onVoteSuccess, onBackClick }) {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [hasVoted, setHasVoted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const fetchCandidates = useCallback(async () => {
    try {
      const response = await api.getCandidates(electionId);
      setCandidates(Array.isArray(response) ? response : []);
      
      // Check if user has already voted
      const voteStatus = await api.checkUserVoted(electionId, token);
      if (voteStatus.has_voted) {
        setHasVoted(true);
      }
    } catch (err) {
      setError("Failed to load candidates");
    }
    setLoading(false);
  }, [electionId, token]);

  useEffect(() => {
    fetchCandidates();
  }, [fetchCandidates]);

  const handleVote = async () => {
    // First check if candidate is selected
    if (!selectedCandidate) {
      setError("Please select a candidate");
      return;
    }

    // Check if already voted
    if (hasVoted) {
      setError("You have already voted in this election. One vote per user only.");
      return;
    }

    // Cast the vote directly
    setIsSubmitting(true);
    try {
      const response = await api.castVote(electionId, selectedCandidate.id, token);
      if (response.detail && response.detail.includes("already voted")) {
        setHasVoted(true);
        setError("You have already voted in this election. One vote per user only.");
      } else {
        setHasVoted(true);
        onVoteSuccess();
      }
    } catch (err) {
      const errorMsg = err.message || "Failed to cast vote";
      if (errorMsg.includes("already voted")) {
        setHasVoted(true);
        setError("You have already voted in this election. One vote per user only.");
      } else {
        setError(errorMsg);
      }
    }
    setIsSubmitting(false);
  };

  if (loading) return <div className="loading">Loading candidates...</div>;

  if (hasVoted) {
    return (
      <div className="voting-container">
        <button className="back-button" onClick={onBackClick} title="Go Back">
          ←
        </button>
        <h1>Cast Your Vote</h1>
        <div className="already-voted-message">
          <p>✓ You have already cast your vote in this election!</p>
          <p>Each voter can only vote once per election.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="voting-container">
      <button className="back-button" onClick={onBackClick} title="Go Back">
        ←
      </button>
      <h1>Cast Your Vote</h1>
      {error && <div className="error">{error}</div>}
      
      <div className="voting-content">
        <div className="candidates-grid">
          {candidates.map((candidate, index) => (
            <div
              key={candidate.id}
              className={`candidate-card-simple ${
                selectedCandidate?.id === candidate.id ? "selected" : ""
              }`}
              style={{ "--delay": `${index * 0.1}s` }}
              onClick={() => setSelectedCandidate(candidate)}
            >
              <div className="candidate-symbol">{candidate.symbol_number}</div>
              <div className="candidate-name">{candidate.name}</div>
            </div>
          ))}
        </div>

        {selectedCandidate && (
          <div className="vote-action">
            <button
              className="vote-button"
              onClick={handleVote}
              disabled={!selectedCandidate || hasVoted || isSubmitting}
            >
              {hasVoted ? "Already Voted" : isSubmitting ? "Casting Vote..." : "Submit Vote"}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default VotingPage;
