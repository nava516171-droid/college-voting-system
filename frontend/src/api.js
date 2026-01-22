// Get API URL - use REACT_APP_API_URL or construct from current location
const getApiBaseUrl = () => {
  // If explicitly set, use it
  if (process.env.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }
  
  // For development/mobile access, use the hostname with port 8001
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname;
    // If localhost or 127.0.0.1, keep it for desktop
    // Otherwise use the same hostname for mobile access
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      return 'http://localhost:8001';
    }
    // For IP-based access (mobile), use the same IP with port 8001
    return `http://${hostname}:8001`;
  }
  
  return 'http://10.244.110.136:8001';
};

const API_BASE_URL = getApiBaseUrl();
console.log('API Base URL:', API_BASE_URL);

// Helper function to handle fetch with better error handling
const fetchWithErrorHandling = async (url, options = {}) => {
  try {
    const response = await fetch(url, options);
    const data = await response.json();
    
    if (!response.ok) {
      console.error('API Error:', { status: response.status, data });
      throw new Error(data.detail || `HTTP ${response.status}`);
    }
    
    return data;
  } catch (error) {
    console.error('Fetch Error:', error.message);
    if (error instanceof TypeError) {
      throw new Error(`Cannot connect to server at ${API_BASE_URL}. Make sure the backend is running and the IP address is correct.`);
    }
    throw error;
  }
};

export const api = {
  // Auth
  login: (email, password) =>
    fetchWithErrorHandling(`${API_BASE_URL}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    }),

  loginWithToken: (token) =>
    fetchWithErrorHandling(`${API_BASE_URL}/api/auth/login-with-token?token=${encodeURIComponent(token)}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    }),

  register: (email, password, full_name, roll_number) =>
    fetchWithErrorHandling(`${API_BASE_URL}/api/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password, full_name, roll_number }),
    }),

  // OTP
  requestOTP: (email, token) =>
    fetch(`${API_BASE_URL}/api/otp/request`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email }),
    }).then((r) => {
      if (!r.ok) {
        return r.json().then(data => {
          throw new Error(data.detail || `HTTP ${r.status}: Failed to send OTP`);
        });
      }
      return r.json();
    }),

  verifyOTP: (otp_code, token) =>
    fetch(`${API_BASE_URL}/api/otp/verify`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ otp_code }),
    }).then((r) => {
      if (!r.ok) {
        return r.json().then(data => {
          throw new Error(data.detail || `HTTP ${r.status}: Failed to verify OTP`);
        });
      }
      return r.json();
    }),

  // Elections
  getElections: () =>
    fetch(`${API_BASE_URL}/api/elections`).then((r) => r.json()),

  getElectionById: (id) =>
    fetch(`${API_BASE_URL}/api/elections/${id}`).then((r) => r.json()),

  // Candidates
  getCandidates: (electionId) =>
    fetch(`${API_BASE_URL}/api/elections/${electionId}/candidates`).then((r) =>
      r.json()
    ),

  getAllCandidates: () =>
    fetch(`${API_BASE_URL}/api/candidates/all`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }).then((r) => {
      if (!r.ok) {
        throw new Error(`HTTP ${r.status}: Failed to fetch candidates`);
      }
      return r.json();
    }).catch(err => {
      throw err;
    }),

  // Voting
  castVote: (electionId, candidateId, token) =>
    fetch(`${API_BASE_URL}/api/votes/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        election_id: electionId,
        candidate_id: candidateId,
      }),
    }).then((r) => r.json()),

  checkUserVoted: (electionId, token) =>
    fetch(`${API_BASE_URL}/api/votes/user/${electionId}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    }).then((r) => r.json()),

  // Results
  getResults: (electionId) =>
    fetch(`${API_BASE_URL}/api/votes/election/${electionId}`).then((r) =>
      r.json()
    ),

  // Admin
  adminRegister: (email, full_name, password) =>
    fetch(`${API_BASE_URL}/api/admin/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, full_name, password }),
    }).then((r) => {
      if (!r.ok) {
        return r.json().then(data => {
          throw new Error(data.detail || `HTTP ${r.status}: Registration failed`);
        });
      }
      return r.json();
    }),

  adminLogin: (email, password) =>
    fetch(`${API_BASE_URL}/api/admin/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    }).then((r) => {
      if (!r.ok) {
        return r.json().then(data => {
          throw new Error(data.detail || `HTTP ${r.status}: Login failed`);
        });
      }
      return r.json();
    }),

  getAdminProfile: (token) =>
    fetch(`${API_BASE_URL}/api/admin/profile`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    }).then((r) => {
      if (!r.ok) {
        return r.json().then(data => {
          throw new Error(data.detail || `HTTP ${r.status}: Failed to fetch profile`);
        });
      }
      return r.json();
    }),

  getAdminStatistics: (token) =>
    fetch(`${API_BASE_URL}/api/admin/statistics/dashboard`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    }).then((r) => {
      if (!r.ok) {
        return r.json().then(data => {
          throw new Error(data.detail || `HTTP ${r.status}: Failed to fetch statistics`);
        });
      }
      return r.json();
    }),

  getUsers: (token) =>
    fetch(`${API_BASE_URL}/api/admin/users`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    }).then((r) => {
      if (!r.ok) {
        return r.json().then(data => {
          throw new Error(data.detail || `HTTP ${r.status}: Failed to fetch users`);
        });
      }
      return r.json();
    }),

  // Face Recognition
  registerFace: (imageData, token) =>
    fetch(`${API_BASE_URL}/api/face/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ image_data: imageData }),
    }).then((r) => {
      if (!r.ok) {
        return r.json().then(data => {
          throw new Error(data.detail || `HTTP ${r.status}: Failed to register face`);
        });
      }
      return r.json();
    }),

  verifyFace: (imageData, token) =>
    fetch(`${API_BASE_URL}/api/face/verify`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ image_data: imageData }),
    }).then((r) => {
      if (!r.ok) {
        return r.json().then(data => {
          throw new Error(data.detail || `HTTP ${r.status}: Face verification failed`);
        });
      }
      return r.json();
    }),

  verifyFaceForVoting: (imageData, token) =>
    fetch(`${API_BASE_URL}/api/face/verify-for-voting`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ image_data: imageData }),
    }).then((r) => {
      if (!r.ok) {
        return r.json().then(data => {
          throw new Error(data.detail || `HTTP ${r.status}: Face verification failed`);
        });
      }
      return r.json();
    }),

  // Candidate Portal
  candidateLogin: (email, password) =>
    fetchWithErrorHandling(`${API_BASE_URL}/api/candidate/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    }),

  getCandidateProfile: (candidateId) =>
    fetchWithErrorHandling(`${API_BASE_URL}/api/candidate/profile/${candidateId}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    }),

  updateCandidateProfile: (candidateId, data) =>
    fetchWithErrorHandling(`${API_BASE_URL}/api/candidate/profile/${candidateId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }),
};
