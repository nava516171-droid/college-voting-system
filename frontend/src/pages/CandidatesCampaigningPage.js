import React, { useState, useEffect, useCallback } from "react";
import { api } from "../api";
import "../styles/CandidatesCampaigningPage.css";

function CandidatesCampaigningPage({ token, electionId, onBackClick }) {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedCandidate, setSelectedCandidate] = useState(null);

  const fetchCandidates = useCallback(async () => {
    try {
      const response = await api.getCandidates(electionId);
      setCandidates(Array.isArray(response) ? response : []);
    } catch (err) {
      setError("Failed to load candidates");
    }
    setLoading(false);
  }, [electionId]);

  useEffect(() => {
    fetchCandidates();
  }, [fetchCandidates]);

  if (loading) return <div className="loading">Loading candidates...</div>;

  return (
    <div className="campaigning-container">
      <button className="back-button" onClick={onBackClick} title="Go Back">
        ←
      </button>
      <h1>Candidates Campaigning</h1>
      {error && <div className="error">{error}</div>}

      <div className="campaigning-content">
        <div className="candidates-list">
          {candidates.map((candidate) => (
            <div
              key={candidate.id}
              className={`campaign-card ${
                selectedCandidate?.id === candidate.id ? "active" : ""
              }`}
              onClick={() => setSelectedCandidate(candidate)}
            >
              <div className="candidate-header">
                <div className="symbol">{candidate.symbol_number}</div>
                <div className="candidate-info">
                  <h3>{candidate.name}</h3>
                  <p className="party-name">{candidate.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {selectedCandidate && (
          <div className="campaign-details">
            <div className="detail-header">
              <div className="detail-symbol">{selectedCandidate.symbol_number}</div>
              <div className="detail-title">
                <h2>{selectedCandidate.name}</h2>
                <p>{selectedCandidate.description}</p>
              </div>
            </div>
            
            {selectedCandidate.poster && (
              <div className="info-section">
                <h3>Campaign Poster</h3>
                <img 
                  src={selectedCandidate.poster} 
                  alt={`${selectedCandidate.name}'s campaign poster`}
                  className="campaign-poster-image"
                />
              </div>
            )}
            
            <div className="campaign-info">
              <div className="info-section">
                <h3>Campaign Platform</h3>
                <p>
                  {selectedCandidate.campaign_message || 
                   "Working towards a better college experience for all students. Focused on student welfare, academic excellence, and campus development."}
                </p>
              </div>

              <div className="info-section">
                <h3>Key Initiatives</h3>
                <ul>
                  <li>Student Welfare Programs</li>
                  <li>Academic Support Services</li>
                  <li>Campus Infrastructure Development</li>
                  <li>Student Engagement Activities</li>
                </ul>
              </div>

              <div className="info-section">
                <h3>About</h3>
                <p>
                  {selectedCandidate.about || 
                   "A dedicated student leader committed to serving the college community and bringing positive change to campus life."}
                </p>
              </div>
            </div>
          </div>
        )}

        {!selectedCandidate && (
          <div className="campaign-details empty">
            <p>Select a candidate to view their campaign details</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default CandidatesCampaigningPage;
