from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.candidate import Candidate
from app.models.election import Election
from app.models.user import User, UserRole
from app.models.admin import Admin
from app.schemas.candidate import CandidateCreate, CandidateResponse
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/candidates", tags=["candidates"])


@router.get("/all")
def get_all_candidates(db: Session = Depends(get_db)):
    """Get all candidates"""
    try:
        candidates = db.query(Candidate).all()
        result = []
        for c in candidates:
            result.append({
                "id": c.id,
                "name": c.name,
                "election_id": c.election_id,
                "symbol_number": c.symbol_number,
                "description": c.description if c.description else ""
            })
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching candidates: {str(e)}"
        )


@router.post("/", response_model=CandidateResponse)
def create_candidate(
    candidate: CandidateCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new candidate (Admin only)"""
    if current_user.role not in [UserRole.ADMIN, UserRole.ELECTION_OFFICER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )

    # Verify election exists
    election = db.query(Election).filter(
        Election.id == candidate.symbol_number
    ).first()

    db_candidate = Candidate(**candidate.dict())
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate


@router.get("/election/{election_id}", response_model=list[CandidateResponse])
def get_election_candidates(election_id: int, db: Session = Depends(get_db)):
    """Get all candidates for an election"""
    candidates = db.query(Candidate).filter(
        Candidate.election_id == election_id
    ).all()
    return candidates


@router.get("/{candidate_id}", response_model=CandidateResponse)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    """Get candidate by ID"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found"
        )
    return candidate


@router.put("/{candidate_id}", response_model=CandidateResponse)
def update_candidate(
    candidate_id: int,
    candidate: CandidateCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update candidate (Admin only)"""
    if current_user.role not in [UserRole.ADMIN, UserRole.ELECTION_OFFICER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )

    db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not db_candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found"
        )

    for key, value in candidate.dict().items():
        setattr(db_candidate, key, value)

    db.commit()
    db.refresh(db_candidate)
    return db_candidate


@router.delete("/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_candidate(
    candidate_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete candidate (Admin only)"""
    if current_user.role not in [UserRole.ADMIN, UserRole.ELECTION_OFFICER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )

    db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not db_candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found"
        )

    db.delete(db_candidate)
    db.commit()
