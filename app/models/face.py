from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class FaceEncoding(Base):
    __tablename__ = "face_encodings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    face_encoding = Column(LargeBinary, nullable=False)  # Serialized numpy array
    face_image = Column(LargeBinary, nullable=True)  # Optional original image
    confidence_score = Column(Float, default=0.0)  # Face detection confidence
    is_verified = Column(String, default="pending")  # pending, verified, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    verified_at = Column(DateTime, nullable=True)
    last_used_at = Column(DateTime, nullable=True)

    user = relationship("User")

    def __repr__(self):
        return f"<FaceEncoding(id={self.id}, user_id={self.user_id}, status={self.is_verified})>"
