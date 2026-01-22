from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    election_id = Column(Integer, ForeignKey("elections.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    symbol_number = Column(Integer, nullable=False)
    email = Column(String, unique=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    campaign_message = Column(Text, nullable=True)
    about = Column(Text, nullable=True)
    poster = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    election = relationship("Election", back_populates="candidates")
    votes = relationship("Vote", back_populates="candidate")

    def __repr__(self):
        return f"<Candidate(id={self.id}, name={self.name}, election_id={self.election_id})>"
