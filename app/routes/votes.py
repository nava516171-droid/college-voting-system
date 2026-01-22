from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.vote import Vote
from app.models.user import User
from app.models.election import Election
from app.models.candidate import Candidate
from app.models.face import FaceEncoding
from app.schemas.vote import VoteCreate, VoteResponse
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/votes", tags=["votes"])


@router.post("/", response_model=VoteResponse)
def cast_vote(
    vote: VoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Cast a vote for a candidate"""
    
    # Optional: Check if user has face registered (commented out for now)
    # face_record = db.query(FaceEncoding).filter(
    #     FaceEncoding.user_id == current_user.id
    # ).first()
    # if not face_record or face_record.is_verified != "verified":
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Face recognition required")
    
    # Check if election exists and is active
    election = db.query(Election).filter(Election.id == vote.election_id).first()
    if not election:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Election not found"
        )

    if not election.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Election is not active"
        )

    # Check if candidate exists
    candidate = db.query(Candidate).filter(Candidate.id == vote.candidate_id).first()
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found"
        )

    # Check if user already voted in this election
    existing_vote = db.query(Vote).filter(
        Vote.user_id == current_user.id, Vote.election_id == vote.election_id
    ).first()
    if existing_vote:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already voted in this election",
        )

    db_vote = Vote(
        user_id=current_user.id,
        election_id=vote.election_id,
        candidate_id=vote.candidate_id,
    )
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote


@router.get("/election/{election_id}")
def get_election_results(election_id: int, db: Session = Depends(get_db)):
    """Get voting results for an election"""
    election = db.query(Election).filter(Election.id == election_id).first()
    if not election:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Election not found"
        )

    # Get all candidates with their vote counts (including 0 votes)
    results = db.query(
        Candidate.id,
        Candidate.name,
        func.count(Vote.id).label("vote_count"),
    ).outerjoin(
        Vote, (Candidate.id == Vote.candidate_id) & (Vote.election_id == election_id)
    ).filter(
        Candidate.election_id == election_id
    ).group_by(
        Candidate.id, Candidate.name
    ).order_by(
        func.count(Vote.id).desc()
    ).all()

    return [
        {"candidate_id": r[0], "candidate_name": r[1], "vote_count": r[2]}
        for r in results
    ]


@router.get("/user/{election_id}")
def check_user_voted(
    election_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Check if user has already voted in an election"""
    vote = db.query(Vote).filter(
        Vote.user_id == current_user.id, Vote.election_id == election_id
    ).first()
    return {"has_voted": vote is not None}
