# 🚀 Quick Start Guide - College Voting System Backend

## ✅ SYSTEM IS RUNNING!

The backend is **currently running** at: **http://localhost:8000**

---

## 📱 HOW TO TEST THE API

### **Option 1: Interactive Swagger UI (BEST)**
Open this in your browser:
```
http://localhost:8000/docs
```
✅ Try all endpoints with real-time feedback
✅ See all request/response schemas
✅ Auto-generated from code

### **Option 2: Alternative ReDoc**
```
http://localhost:8000/redoc
```

### **Option 3: Command Line (curl)**
```bash
# Health check
curl http://localhost:8000/health

# Register a user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "roll_number": "CS001",
    "email": "test@college.edu",
    "full_name": "John Doe",
    "password": "Pass123"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@college.edu",
    "password": "Pass123"
  }'
```

---

## 🧪 RUN AUTOMATED TESTS

```bash
# In project directory:
cd "c:\Users\Navaneeth M\Desktop\college voting system"

# Activate virtual environment
.\venv\Scripts\activate

# Run all tests
pytest tests/test_api.py -v

# Run specific test
pytest tests/test_api.py::TestAuthentication::test_register_user -v

# Run with coverage
pytest tests/test_api.py --cov=app
```

**Result**: All 15 tests passing ✅

---

## 📝 IMPORTANT ENDPOINTS

### Registration & Login
```
POST   /api/auth/register       - Create new user
POST   /api/auth/login          - Login & get JWT token
```

### OTP Verification
```
POST   /api/otp/request         - Request OTP
POST   /api/otp/verify          - Verify OTP code
GET    /api/otp/status          - Check OTP status
POST   /api/otp/resend          - Resend OTP
```

### Elections Management
```
GET    /api/elections/          - List all elections
POST   /api/elections/          - Create election (admin only)
GET    /api/elections/{id}      - Get election details
PUT    /api/elections/{id}      - Update election (admin only)
DELETE /api/elections/{id}      - Delete election (admin only)
```

### Voting
```
POST   /api/votes/              - Cast a vote
GET    /api/votes/election/{id} - Get election results
GET    /api/votes/user/{id}     - Check if user voted
```

### Candidates
```
POST   /api/candidates/                    - Create candidate
GET    /api/candidates/election/{id}       - Get candidates for election
GET    /api/candidates/{id}                - Get candidate details
PUT    /api/candidates/{id}                - Update candidate
DELETE /api/candidates/{id}                - Delete candidate
```

---

## 🔑 TEST CREDENTIALS (After Registration)

You can use the Swagger UI to register new users, or use test data:

**Example User**:
- Roll Number: `CS2024001`
- Email: `student1@college.edu`
- Name: `Alice Johnson`
- Password: `SecurePass123`

---

## 🛠️ PROJECT STRUCTURE

```
college voting system/
├── app/
│   ├── models/         # Database models (User, Election, etc.)
│   ├── routes/         # API endpoints
│   ├── schemas/        # Request/response validation
│   ├── utils/          # Helper functions (auth, OTP, email)
│   ├── config.py       # Configuration settings
│   └── database.py     # Database connection
├── tests/
│   ├── test_api.py     # Unit tests (15 tests)
│   └── conftest.py     # Test configuration
├── main.py             # Application entry point
├── requirements.txt    # Python dependencies
├── voting_system.db    # SQLite database
└── README.md           # Full documentation
```

---

## 🔐 SECURITY FEATURES

✅ Password hashing with bcrypt
✅ JWT token authentication
✅ OTP verification (6-digit codes)
✅ Role-based access control
✅ Email validation
✅ Duplicate vote prevention
✅ Secure password comparison

---

## 📊 DATABASE

**Type**: SQLite (development/testing)
**File**: `voting_system.db`
**Tables**: 5 (users, elections, candidates, votes, otps)

### To switch to PostgreSQL:
Update `.env` file:
```
DATABASE_URL=postgresql://user:password@localhost:5432/voting_db
```

---

## 🚀 TO RESTART THE SERVER

**If server crashes or needs restart**:

```bash
# Open terminal in project directory
cd "c:\Users\Navaneeth M\Desktop\college voting system"

# Activate virtual environment
.\venv\Scripts\activate

# Run the server
python main.py
```

Server will start at: `http://localhost:8000`

---

## ⚠️ TROUBLESHOOTING

### Q: Server won't start
**A**: Make sure port 8000 is not in use
```bash
# Check what's using port 8000:
netstat -ano | findstr :8000
```

### Q: Tests failing
**A**: Make sure server is running before running tests
```bash
# Terminal 1: Start server
python main.py

# Terminal 2: Run tests
pytest tests/test_api.py -v
```

### Q: OTP not showing
**A**: OTP codes print to server console when requested
```
Check the server terminal where main.py is running
```

### Q: Need to reset database
**A**: Delete the file and restart server
```bash
del voting_system.db
python main.py
```

---

## 📚 FULL DOCUMENTATION

See `README.md` and `VERIFICATION_REPORT.md` for complete information.

---

## ✨ WHAT'S WORKING

| Feature | Status |
|---------|--------|
| User Registration | ✅ |
| User Login | ✅ |
| JWT Authentication | ✅ |
| OTP Generation | ✅ |
| OTP Verification | ✅ |
| Election Management | ✅ |
| Candidate Management | ✅ |
| Voting System | ✅ |
| Vote Prevention (duplicate) | ✅ |
| Election Results | ✅ |
| Error Handling | ✅ |
| Input Validation | ✅ |
| API Documentation | ✅ |
| Unit Tests (15/15) | ✅ |

---

## 🎯 SUMMARY

**Status**: ✅ FULLY FUNCTIONAL

**Server Location**: http://localhost:8000

**API Docs**: http://localhost:8000/docs

**Tests Passing**: 15/15 (100%)

**Ready For**: Testing, Frontend Integration, Deployment

---

**Last Updated**: December 30, 2025
**Version**: 1.0.0
