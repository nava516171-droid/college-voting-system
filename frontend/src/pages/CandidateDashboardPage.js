import React, { useState, useEffect } from "react";
import { api } from "../api";
import "../styles/CandidateDashboardPage.css";

function CandidateDashboardPage({ candidateToken, candidateId, candidateName, onLogout }) {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [campaignMessage, setCampaignMessage] = useState("");
  const [about, setAbout] = useState("");
  const [poster, setPoster] = useState("");
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    fetchProfile();
  }, [candidateId]);

  const fetchProfile = async () => {
    try {
      const response = await api.getCandidateProfile(candidateId);
      setProfile(response);
      setCampaignMessage(response.campaign_message || "");
      setAbout(response.about || "");
      setPoster(response.poster || "");
    } catch (err) {
      setError("Failed to load profile");
    }
    setLoading(false);
  };

  const handlePosterUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Check file type
      if (!['image/jpeg', 'image/png'].includes(file.type)) {
        setError("Please upload a JPEG or PNG image");
        return;
      }
      
      // Check file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        setError("Image size should be less than 5MB");
        return;
      }
      
      // Convert to base64
      const reader = new FileReader();
      reader.onload = (event) => {
        setPoster(event.target.result);
        setError("");
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSave = async () => {
    setIsSaving(true);
    setError("");
    setSuccess("");

    try {
      await api.updateCandidateProfile(candidateId, {
        campaign_message: campaignMessage,
        about: about,
        poster: poster,
      });
      setSuccess("Campaign information updated successfully!");
      fetchProfile();
      setTimeout(() => setSuccess(""), 3000);
    } catch (err) {
      setError(err.message || "Failed to save changes");
    }
    setIsSaving(false);
  };

  if (loading) return <div className="loading">Loading profile...</div>;

  return (
    <div className="candidate-dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>🎯 Candidate Dashboard</h1>
        </div>
      </header>

      <main className="dashboard-main">
        <div className="dashboard-container">
          {/* Profile Card */}
          <div className="profile-card">
            <div className="candidate-header">
              <div className="symbol">{profile?.symbol_number}</div>
              <div className="candidate-info">
                <h2>{profile?.name}</h2>
                <p className="email">{profile?.email}</p>
                <p className="description">{profile?.description}</p>
              </div>
            </div>
          </div>

          {/* Campaign Information Form */}
          <div className="campaign-form-card">
            <h2>📋 Campaign Information</h2>
            
            {error && <div className="error">{error}</div>}
            {success && <div className="success">{success}</div>}

            <div className="form-group">
              <label>Campaign Message</label>
              <textarea
                value={campaignMessage}
                onChange={(e) => setCampaignMessage(e.target.value)}
                placeholder="Write your campaign message..."
                rows="6"
              />
              <small>This is what voters will see about your campaign</small>
            </div>

            <div className="form-group">
              <label>About You</label>
              <textarea
                value={about}
                onChange={(e) => setAbout(e.target.value)}
                placeholder="Tell voters about yourself..."
                rows="6"
              />
              <small>Share your background and qualifications</small>
            </div>

            <div className="form-group">
              <label>Poster Image (JPEG/PNG)</label>
              <input
                type="file"
                accept="image/jpeg,image/png"
                onChange={handlePosterUpload}
              />
              <small>Upload a JPEG or PNG image (max 5MB)</small>
            </div>

            <button 
              className="save-button" 
              onClick={handleSave}
              disabled={isSaving}
            >
              {isSaving ? "Saving..." : "Save Changes"}
            </button>
          </div>

          {/* Preview Card */}
          <div className="preview-card">
            <h2>👁️ Campaign Preview</h2>
            <div className="preview-content">
              <h3>{profile?.name}</h3>
              <p className="role">{profile?.description}</p>
              
              {poster && (
                <div className="preview-section">
                  <h4>Campaign Poster</h4>
                  <img src={poster} alt="Campaign Poster" className="poster-image" />
                </div>
              )}
              
              <div className="preview-section">
                <h4>Campaign Message</h4>
                <p>{campaignMessage || "No campaign message yet"}</p>
              </div>

              <div className="preview-section">
                <h4>About</h4>
                <p>{about || "No information provided yet"}</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default CandidateDashboardPage;
