from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.candidate import Candidate
from app.utils.security import verify_password, get_password_hash, create_access_token
from datetime import timedelta

router = APIRouter(prefix="/api/candidate", tags=["candidate"])


class CandidateLoginRequest(BaseModel):
    email: str
    password: str


class CandidateLoginResponse(BaseModel):
    access_token: str
    token_type: str
    candidate_id: int
    candidate_name: str


class CandidateCampaignUpdate(BaseModel):
    campaign_message: str
    about: str
    poster: str = None


class CandidateProfileResponse(BaseModel):
    id: int
    name: str
    email: str
    description: str
    symbol_number: int
    campaign_message: str
    about: str
    poster: str = None


@router.post("/login", response_model=CandidateLoginResponse)
def candidate_login(credentials: CandidateLoginRequest, db: Session = Depends(get_db)):
    """Candidate login"""
    candidate = db.query(Candidate).filter(Candidate.email == credentials.email).first()
    
    if not candidate or not candidate.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    if not verify_password(credentials.password, candidate.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(
        data={"sub": f"candidate_{candidate.id}"},
        expires_delta=timedelta(hours=24)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "candidate_id": candidate.id,
        "candidate_name": candidate.name
    }


@router.get("/profile/{candidate_id}", response_model=CandidateProfileResponse)
def get_candidate_profile(candidate_id: int, db: Session = Depends(get_db)):
    """Get candidate profile"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    
    return {
        "id": candidate.id,
        "name": candidate.name,
        "email": candidate.email,
        "description": candidate.description or "",
        "symbol_number": candidate.symbol_number,
        "campaign_message": candidate.campaign_message or "",
        "about": candidate.about or "",
        "poster": candidate.poster or ""
    }


@router.put("/profile/{candidate_id}")
def update_candidate_profile(
    candidate_id: int,
    update_data: CandidateCampaignUpdate,
    db: Session = Depends(get_db)
):
    """Update candidate campaign information"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    
    candidate.campaign_message = update_data.campaign_message
    candidate.about = update_data.about
    if update_data.poster:
        candidate.poster = update_data.poster
    db.commit()
    db.refresh(candidate)
    
    return {
        "id": candidate.id,
        "name": candidate.name,
        "email": candidate.email,
        "description": candidate.description or "",
        "symbol_number": candidate.symbol_number,
        "campaign_message": candidate.campaign_message or "",
        "about": candidate.about or "",
        "poster": candidate.poster or ""
    }
