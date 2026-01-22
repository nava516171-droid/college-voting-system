import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from main import app
from app.models.user import User
from app.utils.security import get_password_hash

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# Fixtures
@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user_data():
    return {
        "roll_number": "CS001",
        "email": "student@college.edu",
        "full_name": "John Doe",
        "password": "Test@1234"
    }


@pytest.fixture
def test_user(test_user_data):
    db = TestingSessionLocal()
    user = User(
        roll_number=test_user_data["roll_number"],
        email=test_user_data["email"],
        full_name=test_user_data["full_name"],
        hashed_password=get_password_hash(test_user_data["password"])
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# Authentication Tests
class TestAuthentication:
    
    def test_register_user(self, test_user_data):
        response = client.post("/api/auth/register", json=test_user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert data["roll_number"] == test_user_data["roll_number"]
        assert "id" in data
    
    def test_register_duplicate_email(self, test_user_data, test_user):
        response = client.post("/api/auth/register", json=test_user_data)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]
    
    def test_login_success(self, test_user_data, test_user):
        login_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == test_user_data["email"]
    
    def test_login_wrong_password(self, test_user_data, test_user):
        login_data = {
            "email": test_user_data["email"],
            "password": "wrongpassword"
        }
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]
    
    def test_login_nonexistent_user(self):
        login_data = {
            "email": "nonexistent@college.edu",
            "password": "password123"
        }
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 401


# OTP Tests
class TestOTP:
    
    def test_request_otp(self, test_user):
        response = client.post("/api/otp/request", json={"email": test_user.email})
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["email"] == test_user.email
        assert data["expires_in_minutes"] == 10
    
    def test_request_otp_nonexistent_user(self):
        response = client.post("/api/otp/request", json={"email": "nonexistent@college.edu"})
        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]
    
    def test_verify_otp_invalid(self, test_user):
        # Request OTP first
        client.post("/api/otp/request", json={"email": test_user.email})
        
        # Try to verify with wrong code
        response = client.post("/api/otp/verify", json={
            "email": test_user.email,
            "otp_code": "000000"
        })
        assert response.status_code == 400
        assert "Invalid or expired OTP" in response.json()["detail"]


# Election Tests
class TestElections:
    
    def test_get_all_elections(self):
        response = client.get("/api/elections/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_create_election_unauthorized(self):
        election_data = {
            "title": "Student Council Election 2025",
            "description": "Vote for student council representatives",
            "start_time": "2025-12-31T10:00:00",
            "end_time": "2025-12-31T18:00:00"
        }
        response = client.post("/api/elections/", json=election_data)
        assert response.status_code == 401
    
    def test_get_election_not_found(self):
        response = client.get("/api/elections/999")
        assert response.status_code == 404
        assert "Election not found" in response.json()["detail"]


# Health Check Tests
class TestHealth:
    
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
    
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


# Integration Tests
class TestIntegration:
    
    def test_register_and_login_flow(self, test_user_data):
        # Register
        register_response = client.post("/api/auth/register", json=test_user_data)
        assert register_response.status_code == 200
        
        # Login
        login_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
        login_response = client.post("/api/auth/login", json=login_data)
        assert login_response.status_code == 200
        assert "access_token" in login_response.json()
    
    def test_register_request_otp_verify_flow(self, test_user_data):
        # Register
        register_response = client.post("/api/auth/register", json=test_user_data)
        assert register_response.status_code == 200
        
        # Request OTP
        otp_response = client.post("/api/otp/request", json={"email": test_user_data["email"]})
        assert otp_response.status_code == 200
        
        # Should have OTP in database (in real test, we'd extract it)
        assert "message" in otp_response.json()
