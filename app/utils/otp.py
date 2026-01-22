import pyotp
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.otp import OTP
from app.models.user import User


def generate_otp() -> str:
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))


def create_otp_for_user(db: Session, user_id: int, expiry_minutes: int = 10) -> str:
    """Create a new OTP for a user and return the OTP code"""
    otp_code = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=expiry_minutes)
    
    # Invalidate any previous OTPs for this user
    db.query(OTP).filter(OTP.user_id == user_id, OTP.is_verified == False).delete()
    
    otp = OTP(
        user_id=user_id,
        otp_code=otp_code,
        expires_at=expires_at
    )
    db.add(otp)
    db.commit()
    db.refresh(otp)
    
    return otp_code


def verify_otp(db: Session, user_id: int, otp_code: str) -> bool:
    """Verify OTP for a user"""
    otp = db.query(OTP).filter(
        OTP.user_id == user_id,
        OTP.otp_code == otp_code,
        OTP.is_verified == False
    ).first()
    
    if not otp:
        return False
    
    if otp.is_expired():
        db.delete(otp)
        db.commit()
        return False
    
    otp.is_verified = True
    otp.verified_at = datetime.utcnow()
    db.commit()
    
    return True


def get_latest_otp(db: Session, user_id: int) -> OTP:
    """Get the latest unverified OTP for a user"""
    return db.query(OTP).filter(
        OTP.user_id == user_id,
        OTP.is_verified == False
    ).order_by(OTP.created_at.desc()).first()


def cleanup_expired_otps(db: Session):
    """Delete expired OTPs"""
    db.query(OTP).filter(OTP.expires_at < datetime.utcnow()).delete()
    db.commit()
