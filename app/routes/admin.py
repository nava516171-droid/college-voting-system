"""Admin routes for authentication and management"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from app.database import get_db
from app.models.admin import Admin
from app.models.candidate import Candidate
from app.models.election import Election
from app.schemas.admin import AdminCreate, AdminLogin, AdminResponse, AdminToken
from app.schemas.candidate import CandidateCreate, CandidateResponse
from app.utils.security import get_password_hash, verify_password
from app.config import settings

router = APIRouter(prefix="/api/admin", tags=["admin"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Admin:
    """Get current authenticated admin"""
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        admin_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if admin_id is None or token_type != "admin":
            raise credentials_exception
            
    except:
        raise credentials_exception
    
    admin = db.query(Admin).filter(Admin.id == int(admin_id)).first()
    
    if admin is None:
        raise credentials_exception
    
    return admin


@router.post("/register", response_model=AdminResponse)
def register_admin(
    admin: AdminCreate,
    db: Session = Depends(get_db)
):
    """Register a new admin account"""
    print(f"\n{'='*60}")
    print(f"[ADMIN REGISTER] Registering admin: {admin.email}")
    print(f"{'='*60}")
    
    # Check if admin already exists
    existing_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if existing_admin:
        print(f"[ERROR] Admin already exists: {admin.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin with this email already exists"
        )
    
    # Create new admin
    hashed_password = get_password_hash(admin.password)
    db_admin = Admin(
        email=admin.email,
        full_name=admin.full_name,
        hashed_password=hashed_password
    )
    
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    
    print(f"[OK] Admin registered successfully: {db_admin.email}")
    print(f"{'='*60}\n")
    
    return db_admin


@router.post("/login", response_model=AdminToken)
def login_admin(
    admin_login: AdminLogin,
    db: Session = Depends(get_db)
):
    """Admin login endpoint"""
    print(f"\n{'='*60}")
    print(f"[ADMIN LOGIN] Login attempt for: {admin_login.email}")
    print(f"{'='*60}")
    
    # Find admin by email
    admin = db.query(Admin).filter(Admin.email == admin_login.email).first()
    if not admin:
        print(f"[ERROR] Admin not found: {admin_login.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(admin_login.password, admin.hashed_password):
        print(f"[ERROR] Invalid password for admin: {admin_login.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not admin.is_active:
        print(f"[ERROR] Admin account is inactive: {admin_login.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin account is inactive"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + access_token_expires
    
    to_encode = {
        "sub": str(admin.id),
        "email": admin.email,
        "type": "admin",
        "exp": expire
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    print(f"[OK] Admin logged in successfully: {admin.email}")
    print(f"[OK] Token generated for admin ID: {admin.id}")
    print(f"{'='*60}\n")
    
    return {
        "access_token": encoded_jwt,
        "token_type": "bearer",
        "admin": admin
    }


@router.get("/profile", response_model=AdminResponse)
async def get_admin_profile(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get current admin profile"""
    current_admin = get_current_admin(token=token, db=db)
    return current_admin


@router.get("/users")
async def get_all_users(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get all users (Admin only)"""
    current_admin = get_current_admin(token=token, db=db)
    
    from app.models.user import User
    
    # Get all users from database
    users = db.query(User).all()
    
    return [
        {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "roll_number": user.roll_number,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
        for user in users
    ]


@router.get("/statistics/dashboard")
async def get_dashboard_statistics(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get dashboard statistics - users, elections, candidates, votes (admin only)"""
    current_admin = get_current_admin(token=token, db=db)
    
    from app.models.user import User
    from app.models.election import Election
    from app.models.candidate import Candidate
    from app.models.vote import Vote
    
    # Get counts from database
    total_users = db.query(User).count()
    total_elections = db.query(Election).count()
    total_candidates = db.query(Candidate).count()
    total_votes = db.query(Vote).count()
    
    return {
        "total_users": total_users,
        "total_elections": total_elections,
        "total_candidates": total_candidates,
        "total_votes": total_votes
    }


@router.get("/{admin_id}", response_model=AdminResponse)
async def get_admin(admin_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get admin by ID (admin only)"""
    current_admin = get_current_admin(token=token, db=db)
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found"
        )
    return admin


@router.post("/candidates", response_model=CandidateResponse)
async def admin_add_candidate(
    candidate: CandidateCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Add a candidate to an election (Admin only)"""
    current_admin = get_current_admin(token=token, db=db)
    
    print(f"\n{'='*60}")
    print(f"[ADMIN ADD CANDIDATE] Admin {current_admin.email} adding candidate")
    print(f"[ADMIN ADD CANDIDATE] Election ID: {candidate.election_id}")
    print(f"[ADMIN ADD CANDIDATE] Candidate: {candidate.name}")
    print(f"{'='*60}")
    
    # Verify election exists
    election = db.query(Election).filter(Election.id == candidate.election_id).first()
    if not election:
        print(f"[ERROR] Election not found: {candidate.election_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Election with ID {candidate.election_id} not found"
        )
    
    # Check if candidate with same name already exists in this election
    existing_candidate = db.query(Candidate).filter(
        Candidate.election_id == candidate.election_id,
        Candidate.name == candidate.name
    ).first()
    
    if existing_candidate:
        print(f"[ERROR] Candidate already exists in this election: {candidate.name}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Candidate '{candidate.name}' already exists in this election"
        )
    
    # Create new candidate
    db_candidate = Candidate(
        name=candidate.name,
        election_id=candidate.election_id,
        symbol_number=candidate.symbol_number,
        description=candidate.description,
        email=candidate.email
    )
    
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    
    print(f"[OK] Candidate added successfully: {db_candidate.name} (ID: {db_candidate.id})")
    print(f"[OK] Election ID: {db_candidate.election_id}")
    print(f"[OK] Symbol Number: {db_candidate.symbol_number}")
    print(f"{'='*60}\n")
    
    return db_candidate


@router.post("/elections", status_code=status.HTTP_201_CREATED)
async def create_election(
    election_data: dict,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Create a new election (Admin only)"""
    current_admin = get_current_admin(token=token, db=db)
    
    print(f"\n{'='*60}")
    print(f"[ADMIN CREATE ELECTION] Admin {current_admin.email} creating election")
    print(f"[ADMIN CREATE ELECTION] Election data: {election_data}")
    print(f"{'='*60}")
    
    # Extract name/title and description from the request
    election_title = election_data.get("name") or election_data.get("title")
    election_description = election_data.get("description", "")
    
    if not election_title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Election name/title is required"
        )
    
    # Create new election with required datetime fields
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    
    db_election = Election(
        title=election_title,
        description=election_description,
        start_time=now,
        end_time=now + timedelta(days=1)
    )
    
    db.add(db_election)
    db.commit()
    db.refresh(db_election)
    
    print(f"[OK] Election created successfully: {db_election.title} (ID: {db_election.id})")
    print(f"{'='*60}\n")
    
    return {
        "id": db_election.id,
        "name": db_election.title,
        "title": db_election.title,
        "description": db_election.description
    }
