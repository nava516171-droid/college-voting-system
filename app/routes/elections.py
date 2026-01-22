from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.election import Election
from app.models.candidate import Candidate
from app.models.user import User, UserRole
from app.schemas.election import ElectionCreate, ElectionUpdate, ElectionResponse
from app.schemas.candidate import CandidateResponse
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/elections", tags=["elections"])


@router.post("/", response_model=ElectionResponse)
def create_election(
    election: ElectionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new election (Admin only)"""
    if current_user.role not in [UserRole.ADMIN, UserRole.ELECTION_OFFICER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )

    db_election = Election(**election.dict())
    db.add(db_election)
    db.commit()
    db.refresh(db_election)
    return db_election


@router.get("/", response_model=list)
def get_elections(db: Session = Depends(get_db)):
    """Get all elections"""
    elections = db.query(Election).all()
    # Return a simple dict list that includes id, title, description, and other fields
    result = []
    for election in elections:
        result.append({
            "id": election.id,
            "name": election.title,
            "title": election.title,
            "description": election.description,
            "status": election.status if election.status else None,
            "is_active": election.is_active,
            "created_at": election.created_at.isoformat() if election.created_at else None
        })
    return result


@router.get("/{election_id}", response_model=ElectionResponse)
def get_election(election_id: int, db: Session = Depends(get_db)):
    """Get election by ID"""
    election = db.query(Election).filter(Election.id == election_id).first()
    if not election:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Election not found"
        )
    return election


@router.put("/{election_id}", response_model=ElectionResponse)
def update_election(
    election_id: int,
    election: ElectionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update election (Admin only)"""
    if current_user.role not in [UserRole.ADMIN, UserRole.ELECTION_OFFICER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )

    db_election = db.query(Election).filter(Election.id == election_id).first()
    if not db_election:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Election not found"
        )

    update_data = election.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_election, key, value)

    db_election.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_election)
    return db_election


@router.delete("/{election_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_election(
    election_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete election (Admin only)"""
    if current_user.role not in [UserRole.ADMIN, UserRole.ELECTION_OFFICER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )

    db_election = db.query(Election).filter(Election.id == election_id).first()
    if not db_election:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Election not found"
        )

    db.delete(db_election)
    db.commit()


@router.get("/{election_id}/candidates", response_model=list[CandidateResponse])
def get_election_candidates(election_id: int, db: Session = Depends(get_db)):
    """Get all candidates for an election"""
    candidates = db.query(Candidate).filter(
        Candidate.election_id == election_id
    ).all()
    return candidates
