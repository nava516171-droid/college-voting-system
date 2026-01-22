from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.otp import OTPRequest, OTPVerify, OTPResponse
from app.utils.otp import create_otp_for_user, verify_otp, get_latest_otp
from app.utils.email import send_otp_email
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/otp", tags=["otp"])


@router.post("/request")
def request_otp(request: OTPRequest, db: Session = Depends(get_db)):
    """Request OTP for email verification"""
    print(f"\n{'='*60}")
    print(f"[OTP REQUEST] Received request for email: {request.email}")
    print(f"{'='*60}")
    
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        print(f"[ERROR] User not found for email: {request.email}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    print(f"[OK] User found: {user.full_name} ({user.email})")
    
    # Generate and store OTP
    otp_code = create_otp_for_user(db, user.id)
    print(f"[OK] OTP code generated: {otp_code}")
    
    # Send OTP via email
    print(f"[INFO] Attempting to send OTP email to {user.email}...")
    email_sent = send_otp_email(user.email, otp_code, user.full_name)
    
    if not email_sent:
        print(f"[ERROR] Failed to send OTP email!")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send OTP email"
        )
    
    print(f"[OK] OTP request completed successfully")
    print(f"{'='*60}\n")
    
    return {
        "message": "OTP sent to your email",
        "email": user.email,
        "expires_in_minutes": 10
    }


@router.post("/verify")
def verify_user_otp(data: OTPVerify, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Verify OTP for current user"""
    # Verify the OTP
    is_valid = verify_otp(db, current_user.id, data.otp_code)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    
    return {
        "message": "OTP verified successfully",
        "user_id": current_user.id,
        "email": current_user.email,
        "is_verified": True
    }


@router.get("/status")
def check_otp_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check OTP verification status for current user"""
    otp = get_latest_otp(db, current_user.id)
    
    if not otp:
        return {
            "has_pending_otp": False,
            "message": "No pending OTP"
        }
    
    return {
        "has_pending_otp": True,
        "is_verified": otp.is_verified,
        "is_expired": otp.is_expired(),
        "created_at": otp.created_at,
        "expires_at": otp.expires_at
    }


@router.post("/resend")
def resend_otp(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Resend OTP to current user's email"""
    # Generate new OTP
    otp_code = create_otp_for_user(db, current_user.id)
    
    # Send via email
    send_otp_email(current_user.email, otp_code, current_user.full_name)
    
    return {
        "message": "OTP resent to your email",
        "email": current_user.email,
        "expires_in_minutes": 10
    }
