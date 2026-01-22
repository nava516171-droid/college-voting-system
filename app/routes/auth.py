from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import secrets
from app.database import get_db
from app.models.user import User
from app.models.login_token import LoginToken
from app.schemas.user import UserCreate, UserLogin, TokenResponse, UserResponse
from app.utils.security import (
    verify_password,
    get_password_hash,
    create_access_token,
)
from app.utils.email import send_welcome_email, send_login_link_email
from app.config import settings
from app.utils.otp import create_otp_for_user
from app.utils.email import send_otp_email

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        # Check if email already exists
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
            )

        # Check if roll number already exists
        db_user = db.query(User).filter(User.roll_number == user.roll_number).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Roll number already registered",
            )

        # Create new user
        hashed_password = get_password_hash(user.password)
        db_user = User(
            roll_number=user.roll_number,
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        print(f"\n{'='*60}")
        print(f"[REGISTRATION] User created successfully")
        print(f"  Email: {db_user.email}")
        print(f"  User ID: {db_user.id}")
        print(f"{'='*60}\n")
        
        # Generate login token
        login_token = secrets.token_urlsafe(32)
        login_link_record = LoginToken(
            user_id=db_user.id,
            token=login_token,
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )
        db.add(login_link_record)
        db.commit()
        
        # Send welcome email with login link
        try:
            print(f"\n{'='*60}")
            print(f"[WELCOME EMAIL] Sending welcome email to {db_user.email}...")
            login_url = f"{settings.FRONTEND_URL}/login?token={login_token}"
            send_login_link_email(db_user.email, db_user.full_name, login_url)
            print(f"[WELCOME EMAIL] ✓ Email sent successfully")
            print(f"{'='*60}\n")
        except Exception as email_error:
            print(f"[WELCOME EMAIL] ✗ Error sending welcome email: {str(email_error)}")
            print(f"{'='*60}\n")
        
        # Generate and send OTP for email verification
        otp_code = None
        try:
            print(f"\n{'='*60}")
            print(f"[OTP GENERATION] Generating OTP for {db_user.email}...")
            otp_code = create_otp_for_user(db, db_user.id)
            print(f"[OTP GENERATION] ✓ OTP generated: {otp_code}")
            print(f"[OTP GENERATION] OTP will expire in 10 minutes")
            print(f"{'='*60}\n")
            
            # Send OTP via email
            try:
                print(f"\n{'='*60}")
                print(f"[OTP EMAIL] Sending OTP email to {db_user.email}...")
                email_sent = send_otp_email(db_user.email, otp_code, db_user.full_name)
                
                if email_sent:
                    print(f"[OTP EMAIL] ✓ OTP email sent successfully!")
                    print(f"[OTP EMAIL] User can now verify their email")
                else:
                    print(f"[OTP EMAIL] ✗ Failed to send OTP email")
                    print(f"[OTP EMAIL] User registration is complete but email verification pending")
                print(f"{'='*60}\n")
            except Exception as otp_email_error:
                print(f"[OTP EMAIL] ✗ Error sending OTP email: {str(otp_email_error)}")
                print(f"{'='*60}\n")
                
        except Exception as otp_error:
            print(f"[OTP GENERATION] ✗ Error generating OTP: {str(otp_error)}")
            print(f"[OTP GENERATION] Registration successful but OTP verification unavailable")
            print(f"{'='*60}\n")
            import traceback
            traceback.print_exc()
        
        return db_user
        
    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"[REGISTRATION ERROR] Unexpected error during registration")
        print(f"  Error: {str(e)}")
        print(f"{'='*60}\n")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed. Please try again."
        )


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Login user and return access token"""
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive"
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": db_user,
    }


@router.post("/login-with-token", response_model=TokenResponse)
def login_with_token(token: str, db: Session = Depends(get_db)):
    """Login user using email verification token"""
    login_token = db.query(LoginToken).filter(LoginToken.token == token).first()
    
    if not login_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired login link"
        )
    
    if not login_token.is_valid():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login link has expired. Please register again or request a new link."
        )
    
    db_user = db.query(User).filter(User.id == login_token.user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Mark token as used
    login_token.is_used = True
    login_token.used_at = datetime.utcnow()
    db.commit()
    
    # Create access token
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": db_user,
    }
